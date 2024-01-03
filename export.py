from pysqlcipher3 import dbapi2 as sqlite

def decrypt_database(encrypted_db_path, decrypted_db_path, password):
    con = sqlite.connect(encrypted_db_path)
    con.execute("PRAGMA key = '%s'" % password)
    con.execute("ATTACH DATABASE '%s' AS decrypted_db KEY ''" % decrypted_db_path)
    con.execute("SELECT sqlcipher_export('decrypted_db')")
    con.execute("DETACH DATABASE decrypted_db")
    con.close()

# Usage
encrypted_db_path = './vault/vault.sqlite'
decrypted_db_path = 'your_decrypted_database.db'
password = input('Password: ')
decrypt_database(encrypted_db_path, decrypted_db_path, password)
