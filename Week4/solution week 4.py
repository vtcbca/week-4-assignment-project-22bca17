
def create_contact_table():
    #create table of contact
    cur.execute("create table if not exists contact\
                (\
                fname text,\
                lname text,\
                contact number,\
                email text,\
                city text)")
    print("Contact table create successful")

def create_logtable():
    #create log_table for maintain log_insert operation
    cur.execute("create table if not exists log_insert\
            (\
            fname text,\
            contact number,\
            d_time text\
            );")
    print("log_insert table create successful")

    #create log_update table
    cur.execute("create table if not exists log_update\
                (\
                fname text,\
                lname text,\
                contact number,\
                email text,\
                city text,\
                operation_name text,\
                d_time text\
                )")
    print("log_update table create successful")

    #create log_table for maintain log_delete operation
    cur.execute("create table if not exists log_delete\
            (\
            fname text,\
            contact number,\
            d_time text\
            );")
    print("log_delete table create successful")

def validation_on_insert():
    #create trigger for valid insert record
    cur.execute("""create trigger if not exists validate_insert before insert on contact
	begin
	select
		case
		when new.email not like '%_@_%._%' then  
		raise(abort,'Please check Your Email Address and Re-Enter Correct Email Address')
		when length(new.contact)!=10 then
		raise(abort,'please input valid contact Number')
		end; 
	end;
	""")
    print("validation insert trigger create successful")
    
def insert_record():
    query="insert into contact values(?,?,?,?,?)"
    l=[]
    first_name=input("Enter Your First Name:")
    last_name=input("Enter Your Last Name:")
    contact=int(input("ENter Your Mobile Number: "))
    email=input("Enter Your Email Address:")
    city=input("Enter Your City Name:")
    store=[first_name,last_name,contact,email,city]
    l.append(store)
    cur.executemany(query,l)
    print("Record Inserted Successfully....!")

def update_record():
    print("First_Name\tLast_Name\tContact\tE_mail\tCity")
    column_name=input("Which column You Want To Update?:").lower()
    print()
    print(column_name)
    #here if..elif conditin is used to choose which field you want to update.
    if column_name=='first name':
        old_fname=input("Enter Old Name First:")
        new_fname=input("Enter New Name First:")
        cur.execute(f"update contact set fname='{new_fname}' where fname='{old_fname}'")
        #cur.execute("update contact set fname={} where fname={}".format(new_fname,old_fname))
        print('Record Updated successfully..!')
    elif column_name=='last name':
        old_lname=input("Enter Old Last Name:")
        new_lname=input("Enter New Last Name :")
        cur.execute(f"update contact set lname='{new_lname}' where lname='{old_lname}'")
        #cur.execute("update contact set fname={} where fname={}".format(new_fname,old_fname))
        print('Record Updated successfully..!')
    elif column_name=='contact':
        old_number=int(input('Enter Old Contact Number:'))
        new_number=int(input('Enter New Contact Number:'))
        cur.execute(f"update contact set contact='{new_number}' where contact='{old_number}'")
        print('Record Updated successfully..!')
    elif column_name=='email':
        old_email=input('Enter Old E-mail Number:')
        new_email=input('Enter New E-mail Number:')
        cur.execute(f"update contact set email='{new_email}' where email='{old_email}'")
        print('Record Updated successfully..!')
    elif column_name=='city':
        old_city=input('Enter Old City:')
        new_city=input('Enter New City:')
        cur.execute(f"update contact set city='{new_city}' where city='{old_city}'")
        print('Record Updated successfully..!')
    else:
        print("You selected Wrong Column. Please Enter Valid Column_name to update your records in the database..!")

def delete_record():
    d_row=input("Enter The Fname which record you want to delete?: ")
    cur.execute(f"delete from contact where fname='{d_row}'")
    print('record delete successfully.')

def search_record():
    print("All Records:")
    print()
    print("Fname\tLname")
    print("---------------")
    cur.execute("select * from contact")
    record=cur.fetchall()
    for i in record:
        print('{}\t{}'.format(i[0],i[1]))

    fname=input("Enter The First Name Which Record You Want? :")
    cur.execute(f"select * from contact where fname='{fname}'")
    print()
    print("Fname\tLname\tContact\t\tEmail\t\t\tCity")
    print("-------------------------------------------------------------------")
    fetch_record=cur.fetchall()
    for i in fetch_record:
        print(f'{i[0]}\t{i[1]}\t{i[2]}\t{i[3]}\t{i[4]}')

#menu() is display which action are perform by user.
def menu():
    print("1.Insert Record\
           2.Update Record\
           3.Delete Record\
           4.Search Record")

#main programe execution
import sqlite3 as sql
connection=sql.connect("c://sqlite3//contact_mgmt_system.db")
#print("database created successfully")
cur=connection.cursor()
create_contact_table()
create_logtable()
validation_on_insert()
print()
menu()
print()
choice=1
print()
while choice!=0:
    choice=int(input('Enter Your Choice: '))
    if choice==1:
        insert_record() 
    elif choice==2:
        update_record()
    elif choice==3:
        delete_record()
    elif choice==4:
        search_record()
#in this condition, if you want to break this loop then enter 0 value so loop's can stop.
connection.commit()
connection.close()
