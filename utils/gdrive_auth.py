"""
Google Drive Authentication - Runtime Prompt
Each user authenticates with their own Google account
"""

from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive
import pandas as pd
import io
import os
import requests

class DriveDataLoader:
    """
    Authenticate users at runtime.
    Each person uses their own Google credentials.
    """

    def __init__(self, client_secrets_file='../auth/client_secrets.json'):
        self.drive            = None
        self.user_email       = None
        self._auth_ok         = False   # ← was missing
        self._read_ok         = False   # ← was missing
        self._write_ok        = False   # ← was missing

        if not os.path.exists(client_secrets_file):
            raise FileNotFoundError(
                f"\n{'='*60}\n"
                f"ERROR: {client_secrets_file} not found!\n"
                f"This should be in the auth/ folder.\n"
                f"Please contact the project maintainer.\n"
                f"{'='*60}\n"
            )

        self.client_secrets_file = client_secrets_file

    # ─────────────────────────────────────────────────────────────────────────
    # AUTHENTICATE
    # ─────────────────────────────────────────────────────────────────────────
    def authenticate(self):
        """
        Opens browser for the user to log in with their Google account.
        Saves a token so they only need to do this once per machine.
        """
        print("=" * 60)
        print("GOOGLE DRIVE AUTHENTICATION")
        print("=" * 60)
        print("\n🔐 You will be prompted to log in with your Google account")
        print("📋 Make sure you have access to the THM_Survey_Data folder")
        print("\nSteps:")
        print("  1. Browser will open")
        print("  2. Select your Google account")
        print("  3. Click 'Allow' to grant access")
        print("  4. Return here to continue\n")
        print("=" * 60)

        settings = {
            "client_config_backend":    "file",
            "client_config_file":       self.client_secrets_file,
            "save_credentials":         True,
            "save_credentials_backend": "file",
            "save_credentials_file":    "../auth/token.json",
            "get_refresh_token":        True,
            "oauth_scope": [
                "https://www.googleapis.com/auth/drive",
                "https://www.googleapis.com/auth/userinfo.email"
            ]
        }

        gauth = GoogleAuth(settings=settings)
        gauth.LoadCredentialsFile("../auth/token.json")

        if gauth.credentials is None:
            print("\n→ Opening browser for authentication...")
            print("   (If browser doesn't open, copy the URL shown below)\n")
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            print("\n→ Refreshing expired token...")
            gauth.Refresh()
        else:
            print("\n→ Using saved credentials...")
            gauth.Authorize()

        gauth.SaveCredentialsFile("../auth/token.json")

        self.drive      = GoogleDrive(gauth)
        self.user_email = self._get_user_email(gauth)
        self._auth_ok   = True

        print("\n" + "=" * 60)
        print(f"✓ AUTHENTICATED AS: {self.user_email}")
        print("=" * 60)
        print("\n✓ Ready to load data from Google Drive\n")

        return True

    # ─────────────────────────────────────────────────────────────────────────
    # FULL ONBOARDING CHECK
    # ─────────────────────────────────────────────────────────────────────────
    def run_full_check(self, main_folder_id: str,
                       output_folder_id: str,
                       gdrive_files: dict) -> bool:
        """
        Runs the complete onboarding gate:
          1. Authenticate
          2. Verify read access
          3. Verify write access
          4. Verify all data files
        Returns True only if ALL checks pass.
        """
        print("\n" + "=" * 65)
        print("  FYE PROJECT — GOOGLE DRIVE ACCESS CHECK")
        print("=" * 65 + "\n")

        if not self._auth_ok:
            self.authenticate()

        read_ok  = self.verify_read_access(main_folder_id)
        write_ok = self.verify_write_access(output_folder_id)
        files_ok = self.verify_all_files(gdrive_files)

        print("=" * 65)
        if read_ok and write_ok and files_ok:
            print("  🎉 ALL CHECKS PASSED — You're good to go!")
            print(f"  Authenticated as: {self.user_email}")
        else:
            print("  ❌ SOME CHECKS FAILED — See details above.")
            print("  Contact the project maintainer for access.")
        print("=" * 65 + "\n")

        return read_ok and write_ok and files_ok

    # ─────────────────────────────────────────────────────────────────────────
    # PERMISSION CHECKS
    # ─────────────────────────────────────────────────────────────────────────
    def verify_read_access(self, folder_id: str) -> bool:
        """Confirms the user can read from the Drive folder."""
        self._require_auth()
        print("  🔍 Checking READ access...", end=" ")
        try:
            folder = self.drive.CreateFile({'id': folder_id})
            folder.FetchMetadata()
            file_list = self.drive.ListFile(
                {'q': f"'{folder_id}' in parents and trashed=false"}
            ).GetList()
            self._read_ok = True
            print(f"✅  ({len(file_list)} files visible)")
            return True
        except Exception as e:
            print("❌")
            self._print_access_error("READ", folder_id, e)
            return False

    def verify_write_access(self, output_folder_id: str) -> bool:
        self._require_auth()
        print("  🔍 Checking WRITE access...", end=" ")
        try:
            test_file = self.drive.CreateFile({
                'title':   '__write_test__.txt',
                'parents': [{'id': output_folder_id}]
            })
            test_file.SetContentString("write_test")
            test_file.Upload()

            # Try to delete — but don't fail if delete is not permitted
            try:
                test_file.Delete()
            except Exception:
                # Upload succeeded = write access confirmed
                # Delete may not be permitted depending on folder sharing settings
                pass

            self._write_ok = True
            print("✅")
            return True

        except Exception as e:
            print("❌")
            self._print_access_error("WRITE", output_folder_id, e)
            return False

    def verify_all_files(self, gdrive_files: dict) -> bool:
        """Checks every file ID in config.GDRIVE_FILES is accessible."""
        self._require_auth()
        print("\n  🔍 Verifying all dataset files...")
        all_ok = True
        for name, file_id in gdrive_files.items():
            try:
                f = self.drive.CreateFile({'id': file_id})
                f.FetchMetadata(fields='title,fileSize')
                size_kb = int(f.get('fileSize', 0)) // 1024
                print(f"    ✅  {name:<20} — {f['title']} ({size_kb} KB)")
            except Exception:
                print(f"    ❌  {name:<20} — NOT ACCESSIBLE (ID: {file_id[:25]}...)")
                all_ok = False

        if all_ok:
            print("\n  ✅ All files verified.\n")
        else:
            print("\n  ❌ Some files are inaccessible. Check IDs in config.py\n")
        return all_ok

    # ─────────────────────────────────────────────────────────────────────────
    # DATA LOADING
    # ─────────────────────────────────────────────────────────────────────────
    def read_csv_from_drive(self, file_id: str) -> pd.DataFrame:
        self._require_auth()
        print(f"Loading CSV (ID: {file_id[:20]}...)...", end=" ")
        try:
            file = self.drive.CreateFile({'id': file_id})
            file.FetchMetadata()

            mime = file['mimeType']

            if mime == 'application/vnd.google-apps.spreadsheet':
                # It's a Google Sheet — export as CSV
                import requests
                token    = self.drive.auth.credentials.access_token
                export_url = f"https://docs.google.com/spreadsheets/d/{file_id}/export?format=csv"
                response = requests.get(
                    export_url,
                    headers={'Authorization': f'Bearer {token}'}
                )
                response.raise_for_status()
                df = pd.read_csv(io.StringIO(response.text))

            else:
                # It's a regular uploaded CSV file
                content = file.GetContentString()
                df = pd.read_csv(io.StringIO(content))

            print(f"✓ {df.shape}")
            return df

        except Exception as e:
            print(f"✗ Error: {e}")
            raise

    def read_excel_from_drive(self, file_id: str) -> pd.DataFrame:
        """Read an Excel file directly from Google Drive into a DataFrame."""
        self._require_auth()
        print(f"Loading Excel (ID: {file_id[:20]}...)...", end=" ")
        try:
            file = self.drive.CreateFile({'id': file_id})
            file.FetchContent()
            df = pd.read_excel(io.BytesIO(file.content.getvalue()))
            print(f"✓ {df.shape}")
            return df
        except Exception as e:
            print(f"✗ Error: {e}")
            raise
    
    def read_csv(self, file_id: str, label: str = "") -> pd.DataFrame:
        if label:
            print(f"  [{label}] ", end="")
        return self.read_csv_from_drive(file_id)

    def read_excel(self, file_id: str, label: str = "") -> pd.DataFrame:
        if label:
            print(f"  [{label}] ", end="")
        return self.read_excel_from_drive(file_id)

    # ─────────────────────────────────────────────────────────────────────────
    # OUTPUT UPLOAD
    # ─────────────────────────────────────────────────────────────────────────
    def _get_existing_file_id(self, filename: str, folder_id: str):
        """Check if a file with the same name already exists in the folder."""
        query = (
            f"title='{filename}' and "
            f"'{folder_id}' in parents and "
            f"trashed=false"
        )
        file_list = self.drive.ListFile({'q': query}).GetList()
        return file_list[0]['id'] if file_list else None
    
    def upload_figure(self, local_path: str,
                  folder_id: str,
                  drive_filename: str = None) -> str:
        """Uploads a figure to Drive, overwriting if it already exists."""
        self._require_auth()
        drive_filename = drive_filename or os.path.basename(local_path)
        existing_id    = self._get_existing_file_id(drive_filename, folder_id)

        if existing_id:
            print(f"  ⬆  Overwriting figure: {drive_filename}...", end=" ")
            f = self.drive.CreateFile({'id': existing_id})
        else:
            print(f"  ⬆  Uploading figure: {drive_filename}...", end=" ")
            f = self.drive.CreateFile({'title': drive_filename, 'parents': [{'id': folder_id}]})

        f.SetContentFile(local_path)
        f.Upload()
        print(f"✅  (ID: {f['id'][:20]}...)")
        return f['id']

    def upload_dataframe(self, df: pd.DataFrame,
                     filename: str,
                     folder_id: str) -> str:
        """Uploads a DataFrame as CSV to Drive, overwriting if it already exists."""
        self._require_auth()
        existing_id = self._get_existing_file_id(filename, folder_id)

        if existing_id:
            print(f"  ⬆  Overwriting dataframe: {filename}...", end=" ")
            f = self.drive.CreateFile({'id': existing_id})
        else:
            print(f"  ⬆  Uploading dataframe: {filename}...", end=" ")
            f = self.drive.CreateFile({'title': filename, 'parents': [{'id': folder_id}]})

        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        f.SetContentString(csv_buffer.getvalue())
        f.Upload()
        print(f"✅  (ID: {f['id'][:20]}...)")
        return f['id']

    def upload_file(self, local_path: str,
                folder_id: str,
                drive_filename: str = None) -> str:
        """Uploads any file to Drive, overwriting if it already exists."""
        self._require_auth()
        drive_filename = drive_filename or os.path.basename(local_path)
        existing_id    = self._get_existing_file_id(drive_filename, folder_id)

        if existing_id:
            print(f"  ⬆  Overwriting file: {drive_filename}...", end=" ")
            f = self.drive.CreateFile({'id': existing_id})
        else:
            print(f"  ⬆  Uploading file: {drive_filename}...", end=" ")
            f = self.drive.CreateFile({'title': drive_filename, 'parents': [{'id': folder_id}]})

        f.SetContentFile(local_path)
        f.Upload()
        print(f"✅  (ID: {f['id'][:20]}...)")
        return f['id']

    # ─────────────────────────────────────────────────────────────────────────
    # INTERNAL HELPERS
    # ─────────────────────────────────────────────────────────────────────────
    def _require_auth(self):
        if not self._auth_ok or self.drive is None:
            raise RuntimeError(
                "Not authenticated. Call authenticate() or run_full_check() first."
            )

    def _get_user_email(self, gauth) -> str:
        try:
            token    = gauth.credentials.access_token
            response = requests.get(
                'https://www.googleapis.com/oauth2/v1/userinfo',
                headers={'Authorization': f'Bearer {token}'}
            )
            if response.status_code == 200:
                return response.json().get('email', 'Unknown')
        except Exception:
            pass
        return 'Unknown'

    def _print_access_error(self, mode: str, folder_id: str, error: Exception):
        print(f"\n  {'='*60}")
        print(f"  ❌ {mode} ACCESS DENIED")
        print(f"  {'='*60}")
        print(f"  Authenticated as : {self.user_email}")
        print(f"  Folder ID        : {folder_id}")
        print(f"  Error            : {error}")
        print(f"\n  → Ask the project owner to share the folder with:")
        print(f"    {self.user_email}  (Editor permission for write access)")
        print(f"  {'='*60}\n")
