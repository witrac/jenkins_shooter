# 11b8138de0a1c2695ceeff922eb153d42d
import time
import multiprocessing
import argparse
# from jenkinsapi.jenkins import Jenkins
# import jenkinsapi.api
import jenkins
# import RPi.GPIO as GPIO
# GPIO.setmode(GPIO.BCM)
green_led = 4
red_led = 17
# GPIO.setup(green_led, GPIO.OUT)
# GPIO.setup(red_led, GPIO.OUT)
jenkins_username = None
jenkins_password = None

def get_server_instance():
    jenkins_url = 'url'
    # server = jenkinsapi.api.get_latest_build(jenkins_url, "master", username=jenkins_username, password=jenkins_password, ssl_verify=False)
    server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    return server

def get_job_building( server ):
    """Get job details of each job that is running on the Jenkins instance"""
    # Refer Example #1 for definition of function 'get_server_instance'
    # server = get_server_instance()
    # if server.is_running():
    #     return "running"
    # if server.is_good():
    #     return "good"
    result = None
    jobs = server.get_jobs()
    n_branches = len(jobs)
    print( n_branches )
    for job in jobs:
        color = job["color"]
        if "anime" in color:  
            result = job
            break
    return result
    # return "fail"
    # for job_name, job_instance in server.get_jobs():
    #     print ('Job Name:%s' % (job_instance.name))
    #     print ('Job Description:%s' % (job_instance.get_description()))
    #     print ('Is Job running:%s' % (job_instance.is_running()))
    #     print ('Is Job enabled:%s' % (job_instance.is_enabled()))

def get_job_details( server, job ):
    print( job["name"])
    next_build = server.next_build_number = server.get_job_info(job["name"])['nextBuildNumber']
    job_details = server.get_build_info(job["name"], next_build - 1)
    # print(job_details)
    # print(job_details["actions"][0]["causes"][0]["userName"])
    # print(job_details["changeSets"][0]["items"][0]["authorEmail"])
    print(job_details["building"])
    print(job_details["result"])

def blink():
    while True:
        # # GPIO.output(green_led, GPIO.LOW)
        # # GPIO.output(red_led, GPIO.HIGH)
        time.sleep(0.5)
        # # GPIO.output(green_led, GPIO.HIGH)
        # # GPIO.output(red_led, GPIO.LOW)
        time.sleep(0.5)
        print("blink...")

def green():
    print("GREEN")
    # # GPIO.output(green_led, GPIO.HIGH)
    # # GPIO.output(red_led, GPIO.LOW)

def red():
    print("RED")
    # # GPIO.output(green_led, GPIO.LOW)
    # # GPIO.output(red_led, GPIO.HIGH)

def main():
    # p = multiprocessing.Process(target=blink)
    t = 10
    server = get_server_instance()
    job_building = None
    while True:
        job = get_job_building( server )
        if job:
            job_building = job
        if job_building:
            print("--->",job)
            get_job_details( server, job )
        # print(result)
        # if result == "running" and p.is_alive() == False:
        #     p = multiprocessing.Process(target=blink)
        #     p.start()
        #     t = 10
        # elif result == "good":
        #     if p.is_alive():
        #         p.terminate()
        #     green()
        #     t = 30
        # elif result == "fail":
        #     if p.is_alive():
        #         p.terminate()
        #     red()
        #     t = 30
        # else:
        #     print("Compilando...")
        time.sleep(t)
    return 1

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", dest="username", help="Usuario de Jenkins")
    parser.add_argument("-p", "--password", dest="password", help="Contrasenya de Jenkins")
    args = parser.parse_args()
    # Check user and pass exists.
    if not args.username or not args.password:
        raise RuntimeError("username or pasword not specified. Use --help for details")
    global jenkins_username
    jenkins_username = args.username
    global jenkins_password
    jenkins_password = args.password
if __name__ == '__main__':
    parse_args()
    exit(main())