def main():
    
     
    #sqltemplate="select txn_id, customer_id, txn_request_num, last_updt_ts from txn_proc_bfr where regexp_like(txn_data_Clob,'{\"hello\")and txn_status_cd = 'COMPLETED' and txn_type_cd = 'AUTO_SUBMIT' and prim_data_master_src_ref_num = 'Migrate To FIFA' and secndy_data_master_src_ref_num = 'submitterProcessFIFA'"\\
    
    sqltemplate="select '$input$' as BillingId, txn_id, customer_id, txn_request_num, last_updt_ts from txn_proc_bfr where regexp_like(txn_data_Clob,'\{\"name\":\"sourcePCid\",\"charactersticValue\":\\[\\{\"value\":\"$input$\"\\}\\]\\}') and txn_status_cd = 'COMPLETED' and txn_type_cd = 'AUTO_SUBMIT' and prim_data_master_src_ref_num = 'Migrate To FIFA' and secndy_data_master_src_ref_num = 'submitterProcessFIFA'"
    print("sqltemplate=",sqltemplate)
 
				
if __name__ == "__main__":
    main()