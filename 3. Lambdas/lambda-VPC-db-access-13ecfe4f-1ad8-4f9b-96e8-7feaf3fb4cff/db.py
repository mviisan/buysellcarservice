import sys
import logging
#import rds_config
import pymysql
#rds settings
rds_host  = rds_config.instance_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = pymysql.connect(host=rds_host, user=name, passwd=password, db=db_name, connect_timeout=20)
except pymysql.MySQLError as e:
    logger.error("ERROR: Unexpected error: Could not connect to MySQL instance.")
    logger.error(e)
    sys.exit()
logger.info("SUCCESS: Connection to RDS MySQL instance succeeded")

def handler(event, context):
    
    #1 Read the input parameters
    buySell = event["buysell"]
    price   = event["price"]
    car     = event["car"]
    message = event["message"]
    email   = event["email"]
    phone   = event["phone"]
 

    item_count = 0
    vpc_response = ""

    with conn.cursor() as cur:
        # Add table if it doesn't exist already
        cur.execute("create table if not exists CarSale ( CarID  int NOT NULL AUTO_INCREMENT, BuySell varchar(255) NOT NULL, Price varchar(255), Car varchar(255), Announcement varchar(255), Email varchar(255), Phone varchar(255), PRIMARY KEY (CarID))")

        # Check if customer is trying to sell or buy and add announcent or return number of existing cars
        if (buySell == "sell"):
            cur.execute("insert into CarSale (BuySell, Price, Car, Announcement, Email, Phone) values(%s, %s, %s, %s, %s, %s)", (buySell, price, car, message, email, phone))
            conn.commit()
            vpc_response = "We added your sell announcement to the database."
        else :    
            cur.execute("select * from CarSale where car = %s and price = %s", (car, price))
            for row in cur:
                item_count += 1
                logger.info(row)
            vpc_response = ("We found %s cars matching your criteria." %(item_count))
    conn.commit()

    #print("Added %d items from RDS MySQL table" %(item_count))

    #4 Format and return the result
    return {
        'VPC_message'       :   vpc_response
    }