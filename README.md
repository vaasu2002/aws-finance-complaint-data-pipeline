
## **Steps to make lambda function**
The code [lambda_function.py](./lambda_function_code/lambda_function.py) is inside [lambda_function_code](./lambda_function_code) folder
#### **1)** Creating conda environment
```bash
conda create -p env python==3.9 -y
```

#### **2)** Activing conda environment
```bash
source activate ./env
```
#### **3)** Installing all dependencies
```bash
pip install -r requirements.txt
```

#### **4)** Using linux machine to make lambda function files
```bash
pip install --platform manylinux2014_x86_64 --target=lambda_function_code --implementation cp --python==3.9 --only-binary=:all: --upgrade pymongo[srv] boto3 requests
```
#### **5)** Ziping the `lambda_function_code` folder
#### **6)** Uploading lambda files in lambda function console code section
#### **7)** Add all environment variables to the lambda function
-   DATABASE_NAME 
-   COLLECTION_NAME 
-   BUCKET_NAME
-   MONGODB_URL
#### **8)** Adding trigger to lambda function
-   Add trigger EventBridge (CloudWatch Events) to invoke lambda function weekly
-   Schedule expression: `cron(27 15 ? * MON-FRI *)`
