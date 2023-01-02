COPY . /app
RUN pip install -r requirements.txt
RUN apt-get update
RUN curl -O https://s3.us-west-2.amazonaws.com/amazon-eks/1.24.7/2022-10-31/bin/linux/amd64/kubectl
RUN chmod +x ./kubectl
RUN mkdir -p $HOME/bin && cp ./kubectl $HOME/bin/kubectl && export PATH=$PATH:$HOME/bin
RUN mv kubectl /usr/local/bin/
RUN kubectl version --short --client
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
RUN unzip awscliv2.zip
RUN ./aws/install -i /usr/local/aws-cli -b /usr/local/bin
RUN region=$(aws ec2 describe-availability-zones --output text --query 'AvailabilityZones[0].[RegionName]')
RUN echo $region
RUN cluster_name = $(aws eks list-clusters --query 'clusters[0]' --output text)
RUN echo $cluster_name
RUN aws eks update-kubeconfig --name $cluster_name --region $region
#RUN aws eks update-kubeconfig --name radio-dev-ekstask1 --profile default --region us-east-1
#aws eks update-kubeconfig --name <cluster-name> --profile <profile-name> --region <region-name>
# ACCOUNT_ID=$(aws sts get-caller-identity --query "Account" --output text)
# Run app.py when the container launches
CMD ["python", "test.py"]
