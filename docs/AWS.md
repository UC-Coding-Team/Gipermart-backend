# Deployed on a Cloud Platform AWS

Architecture diagram

[![arch.jpg](https://i.postimg.cc/fbNyZ89W/arch.jpg)](https://postimg.cc/K10xDrfC)

Deployments on two Amazon Web services EC2 machines in eu-west-1, type large and type medium.

-   t2.medium:

        - vCPU -> 2	
        -  Mem (GiB) -> 4

-   t2.large:	

        - vCPU -> 2	
        -  Mem (GiB) -> 8

To have access between machines and make API request, we will 
define security gruop where the inbound rules include the IP of the public VPN of both EC2 with the port :8000, :5601, :9200, TCP type.

In the configuration with Django and Elasticsearch it is important to add the host, port and credentials so that they can communicate, and in its defect to open the port of the machine of the EC2 of Elasticsearch through the security group so that it can make the consultations.



