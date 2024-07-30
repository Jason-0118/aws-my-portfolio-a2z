# aws-my-portfolio-a2z

## VPC setting
- Use CloudFormation (cf.yaml) to create VPC with two public subnets and two private subnet.
- ![Screenshot 2024-07-26 at 2 53 27 PM](https://github.com/user-attachments/assets/7cdaeed1-1f47-4417-9aaf-1445926e27fd)

## EFS creating
- Create a EFS and select two AZs so that all instances been launched in these two AZ can access the EFS
  - In instance, make sure change ownership for instance upload and delete file
    - sudo chown -R $USER:$USER /mnt/efs/fs1
    - sudo chmod -R 775 /mnt/efs/fs1

## EC2-client
- Creating EC2 instance
  - Networking settings: Select a public subnet, security group
  - -<img width="1178" alt="Screenshot 2024-07-26 at 3 13 19 PM" src="https://github.com/user-attachments/assets/e5797734-89a5-4a78-8a28-e4620f4271dd">

  - Confugure storage: edit file system(EFS)
- Initial Configuration - SSH into instance
  - sudo yum install nginx
  - sudo systemctl start nginx
  - sudo systemctl enable nginx
  - sudo systemctl status nginx
  - cd /usr/share/nginx/html
- Configure nginx.conf file

## EC2-server
- Creating EC2 instance
  - Networking settings: Select a private subnet, security group
  - <img width="1193" alt="Screenshot 2024-07-26 at 3 12 47 PM" src="https://github.com/user-attachments/assets/c07f3373-5dd5-4012-9af0-45581a80afa3">

  - Confugure storage: edit file system(EFS)
- Initial Configuration - SSH into instance
  - sudo yum install nginx
  - sudo yum install python3-pip
  - sudo pip3 install flask
  - ### before run python3 app.py
    - sudo mkdir /var/log/flask_app
    - sudo chown ec2-user:ec2-user /var/log/flask_app
 
  - sudo systemctl start nginx
  - sudo systemctl enable nginx
  - sudo systemctl status nginx
  - cd /usr/share/nginx/html

## Create ALb & target group
- create ALb sg
- <img width="1195" alt="Screenshot 2024-07-26 at 3 14 20 PM" src="https://github.com/user-attachments/assets/4f2a51e3-6b78-41fe-9583-ed1fd1984e16">

## useful command
- lsof -i -P -n | grep LISTEN
- install node for linux2: https://repost.aws/questions/QUvkkhY--uTiSDkS6R1jFnZQ/node-js-18-on-amazon-linux-2

## demo
- ### Home
 ![home](https://github.com/user-attachments/assets/44465ea9-b6dd-4a12-9b17-ef8a7329409b)
- ### Login
 ![login](https://github.com/user-attachments/assets/58618a20-a0b9-42ac-bf7c-fdefa7f16398)
- ### upload
 ![upload](https://github.com/user-attachments/assets/95485016-13b3-47cf-bc1d-6dafe1a5a785)
- ### delete
 ![delete](https://github.com/user-attachments/assets/13d7a525-93d6-43ea-86a1-a1d82a3a0f58)
- ### restore
 ![restore](https://github.com/user-attachments/assets/53a8d9ce-e94d-45f3-a520-b400ccb1447f)

