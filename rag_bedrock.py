import boto3
import botocore.config
import json
from datetime import datetime




def project_plan_generater(objective:str)-> str:
    

    # Start a conversation with the user message.
    prompt = f"""<s>[INST]
    "I am managing a project with the objective of {objective}. 
    The project must be completed within 2 hours. Can you provide a detailed, 
    step-by-step guide outlining the key tasks, milestones, and timelines needed to successfully achieve this objective? 
    Please include recommendations for managing resources, potential risks, and tips for staying on track throughout the project.
    Make sure all instruction are in 256 word count limit"
    Assitant:[/INST]
    
    """
    body = {
        "prompt":prompt,
        "max_gen_len": 512,
        "top_p": 0.8,
        "temperature": 0.7

    }


    try:
     
        session = boto3.Session(
        aws_access_key_id= "YOUR_AWS_ACCESS_ID",
        aws_secret_access_key= "YOUR_AWS_SECRET_KEY")

        bedrock = session.client('bedrock-runtime', 
                                 region_name='us-east-1',
                                 config=botocore.config.Config(read_timeout = 300,retries = {"max_attempts":3}),
                                )
        response = bedrock.invoke_model( body=json.dumps(body),
            modelId="meta.llama3-70b-instruct-v1:0"
            
        ) 
        
        response_content  = response.get('body').read()
        response_data=json.loads(response_content)
        project_plan = response_data['generation']
        return project_plan
    except Exception as e:
        print(f"Error generating the project {e}")
        return ""
         

def save_plan(bucket, key, generate_plan):
    s3=boto3.client('s3')

    try:
        s3.put_object(Bucket = bucket, Key=key, Body = generate_plan )
        print("data saved to s3")
    except Exception as e:
        print(f"Error while saving data in s3 {e}")


def lambda_handler(event, context):
    objective = list(event.values())[0]
    
    #print(event)
    generate_plan = project_plan_generater(objective=objective)

    if generate_plan:
        current_time = datetime.now().strftime('%H%M%S')
        s3_key = f"planner_output/{current_time}.txt"
        s3_bucket = f"aws-bedrock-demo"
        save_plan(s3_bucket, s3_key, generate_plan)
    else:
        print("No blog was generated")

    return {
        'statusCode': 200,
        'body': json.dumps(f'Project plan has been generated!\n {generate_plan}')
    }


# objective = "Building Advanced RAG With Multiple Data Source Using Langchain"
# generate_plan = project_plan_generater(objective=objective)
# print(generate_plan)

            