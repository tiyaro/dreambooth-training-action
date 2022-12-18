import requests
import os
import sys

url = "https://control.tiyaro.ai/graphql"

apiKey = os.getenv("TIYARO_API_KEY")
if apiKey is None:
    print("Set your TIYARO_API_KEY env variable")
    sys.exit(1)

def get_new_jobId():
    query = """mutation
    {{
        newJobID(jobType: dreambooth) 
    }}
    """
    query = query.format()
    payload = {"variables": {}, "query": query}

    headers = {
        "content-type": "application/json",
        "authorization": f"{apiKey}"
    }

    print('--- Getting new jobId ---')
    response = requests.request("POST", url, json=payload, headers=headers)
    print(f'> API response status: {response.status_code}')
    print(f'> raw response: {response.text}')
    jobId = response.json()['data']['newJobID']
    print(f'> new JobId: {jobId}')
    return jobId

def get_upload_url(job_id, zip_filename):
    query = """query
    {{
        getJobInputURL(jobID: "{0}", objName: "{1}")
    }}
    """
    query = query.format(job_id, zip_filename)
    payload = {"variables": {}, "query": query}

    headers = {
        "content-type": "application/json",
        "authorization": f"{apiKey}"
    }

    print('--- Getting data upload url ---')
    response = requests.request("POST", url, json=payload, headers=headers)
    print(f'> API response status: {response.status_code}')
    # print(f'> raw response: {response.text}')
    uploadUrl = response.json()['data']['getJobInputURL']
    print(f'> Data Upload URL: {uploadUrl}')
    return uploadUrl

def upload_zip_file(file_path, url):
    headers = { 'Content-Type': 'application/octet-stream'}
    print(f'--- Uploading {file_path} to URL')
    response = requests.request("PUT", url, data=open(file_path, 'rb'), headers=headers)
    print(f'> API response status: {response.status_code}')

# for more fine-grained training extend this method, docs: https://tiyaro-api.readthedocs-hosted.com/en/latest/dreambooth.html#start-training-job
def start_dreambooth_training(job_id, name, version, file_name, class_prompt, instance_prompt):
    query = """mutation
    {{
        startTrainingJob
        (
            jobID: "{0}"
            input: {{
                jobType: dreambooth
                dreamboothInput: {{
                    name: "{1}",
                    version: "{2}",
                    datasetS3ObjName: "{3}",

                    instance_prompt: "{4}",
                    class_prompt: "{5}",

                }}
            }}
        ) 
    }}"""
    query = query.format(job_id, name, version, file_name, instance_prompt, class_prompt)
    payload = {"variables": {}, "query": query}

    headers = {
        "content-type": "application/json",
        "authorization": f"{apiKey}"
    }

    print('--- Starting Dreambooth training ---')
    response = requests.request("POST", url, json=payload, headers=headers)
    print(f'> API response status: {response.status_code}')
    print(f'> raw response: {response.text}')


def get_job_status(job_id):
    query = """query
    {{
        getJobStatus(jobID: "{0}") 
        {{
            statusEnum
            errMsg
            created
            finished
        }}
    }}"""
    query = query.format(job_id)
    payload = {"variables": {}, "query": query}

    headers = {
        "content-type": "application/json",
        "authorization": f"{apiKey}"
    }

    print('--- Getting job status ---')
    response = requests.request("POST", url, json=payload, headers=headers)
    print(f'> API response status: {response.status_code}')
    print(f'> raw response: {response.text}')
    status = response.json()['data']['getJobStatus']['statusEnum']
    print(f'> Status: {status}')
    return status

def get_trained_model(job_id):
    query = """query
    {{
        getTrainedModels(jobID: "{0}") 
        {{
            url
            modelCard
        }}
    }}"""
    query = query.format(job_id)
    payload = {"variables": {}, "query": query}

    headers = {
        "content-type": "application/json",
        "authorization": f"{apiKey}"
    }

    print('--- Getting trained model ---')
    response = requests.request("POST", url, json=payload, headers=headers)
    print(f'> API response status: {response.status_code}')
    print(f'> raw response: {response.text}')
    trained_models = response.json()['data']['getTrainedModels']
    if len(trained_models) > 0:
        print(f'> Model URL: {trained_models[0]["url"]}')
        print(f'> Model Card: {trained_models[0]["modelCard"]}') 
    else:
        print('WARN - try again later once training is successful')


if __name__ == '__main__':
    input_file_name = 'input.zip' # created via github action
    input_file_path = f'./{input_file_name}'
    if not os.path.exists(input_file_path):
        raise ValueError(f'input file {input_file_path} does not exist')
    
    if len(sys.argv) != 4:
        print("Usage: main.py <model_name> <instance-prompt> <class-prompt>")
        sys.exit(1)
    
    name_of_retraining_model = sys.argv[1]
    ins_prompt = sys.argv[2]
    clz_prompt = sys.argv[3]

    print(f'--- Starting Dreambooth training for {name_of_retraining_model} ---')
    print(f'> Instance Prompt: {ins_prompt}')
    print(f'> Class Prompt: {clz_prompt}')

    # 1. Get new job_id
    job_id = get_new_jobId()

    # 2. Get upload url
    upload_url = get_upload_url(job_id, input_file_name)

    # 3. Upload data
    upload_zip_file(input_file_path, upload_url)

    # 4. Start training
    # for more fine-grained training extend this method, docs: https://tiyaro-api.readthedocs-hosted.com/en/latest/dreambooth.html#start-training-job
    start_dreambooth_training(
        job_id=job_id,
        name=name_of_retraining_model,
        version='1.0',
        file_name=input_file_name,
        instance_prompt=ins_prompt,
        class_prompt=clz_prompt
    )

    # 5. Get job status
    get_job_status(job_id)
    
    # 7. Get trained models
    get_trained_model(job_id)
