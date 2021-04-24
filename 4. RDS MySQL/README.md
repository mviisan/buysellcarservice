CLI command to deploy RDS instance:

aws rds create-db-instance --db-name ExampleDB --engine MySQL \
--db-instance-identifier MySQLForLambdaTest --backup-retention-period 3 \
--db-instance-class db.t2.micro --allocated-storage 5 --no-publicly-accessible \
--master-username username --master-user-password password


RDS and VPC lambda need to be in the same VPC to communicate
RDS MySQL instance's security group needs to permit inbound traffic on port 3306:

![alt text](https://github.com/mviisan/buysellcarservice/blob/master/RDS%MySQLrds_SG.png?raw=true)