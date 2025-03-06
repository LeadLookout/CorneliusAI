# FILE: cornelius_os/app/modules/developer_mode.py
# FILE: cornelius_os/app/modules/developer_mode.py
import hashlib

class DeveloperMode:
    def __init__(self, password):
        #NEVER STORE A PASSWORD IN PLAIN TEXT, HASH IT!
        self.password_hash = hashlib.sha256(password.encode('utf-8')).hexdigest()
        self.is_enabled = False;

    def authenticate(self, entered_password):
        """Authenticates the developer based on a password."""
        entered_hash = hashlib.sha256(entered_password.encode('utf-8')).hexdigest()
        if entered_hash == self.password_hash:
            self.is_enabled = True
            print("Developer mode enabled.")
            return True
        else:
            self.is_enabled = False
            print("Incorrect password. Developer mode not enabled.")
            return False
        
    def check_access(self,required_trait=None, threshold=None):
        """
        Checks if developer mode is enabled, or a personality trait is
        """
        from .personality import personality # type: ignore #Import here to prevent circular

        if self.is_enabled:
            return True

        if required_trait is not None and threshold is not None:
                trait_value = personality.get_trait(required_trait)
                if trait_value >= threshold:
                    return True
                else:
                    print(f"Access Denied: Insufficient {required_trait} level.")
                    return False

        print("Access Denied: Developer mode is not enabled.")
        return False