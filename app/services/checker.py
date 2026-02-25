import hashlib

class FlagService:
    @staticmethod
    def verify_flag(submitted_flag: str, correct_flag_hash: str) -> bool:
        submitted_hash = hashlib.sha256(submitted_flag.encode()).hexdigest()
        return submitted_hash == correct_flag_hash

# usage: result = FlagService.verify_flag("CTF{n1ce_try}", "stored_hash_here")
