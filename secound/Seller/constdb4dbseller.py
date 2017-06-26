createtable4seller = ("""CREATE TABLE IF NOT EXISTS sellercharacteristic{table4seller}(
                     `seller_no` int(12) NOT NULL AUTO_INCREMENT,
                     `seller_value` Text not NULL,
                     `seller_uid` Text not NULL,
                     `u_id` Text not NULL,
                     PRIMARY KEY(seller_no));""")

befor_select_all_seller = ("""SET block_encryption_mode = 'aes-256-cbc';
                          SET @key_str = SHA2('My secret passphrase',512); 
                          SET @init_vector = 'h>1&cr!a[v+qm&3b+F6*P~'; """)


select_all_seller = ("select AES_DECRYPT(seller_uid,@key_str, @init_vector), AES_DECRYPT(seller_value,@key_str, @init_vector) from sellercharacteristic{table4seller};")


table_check = ("""select AES_DECRYPT(`{seller_uid}`,@key_str, @init_vector), AES_DECRYPT(`{seller_value}`,@key_str, @init_vector) from sellercharacteristic{table4seller};""")

insertableseller = ("""SET @seller_uid = {seller_uid};
                       SET @seller_value = {seller_value};
                       INSERT IGNORE INTO sellercharacteristic(`seller_uid`,`seller_value`) VALUES(AES_ENCRYPT(@seller_uid,@key_str, @init_vector), AES_ENCRYPT(@seller_value,@key_str, @init_vector));""")
            
