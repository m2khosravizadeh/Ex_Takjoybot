sqlـstore = ("CREATE TABLE IF NOT EXISTS close_store_table("
             "`emp_no` int(12) NOT NULL AUTO_INCREMENT,"
             "`stores` Text not NULL,"
             "PRIMARY KEY(emp_no));")

befor_select_all_store = ("SET block_encryption_mode = 'aes-256-cbc';"
                          "SET @key_str = SHA2('My secret passphrase',512); "
                          "SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; ")




select_all_store = ("select AES_DECRYPT(stores,@key_str, @init_vector) from close_store_table;")


table_check = ("""select AES_DECRYPT(`{column}`,@key_str, @init_vector) from {table_seller};""")

