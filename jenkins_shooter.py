import time
import argparse
import jenkins
import paho.mqtt.client as mqtt

jenkins_username = None
jenkins_password = None

def get_server_instance():
    jenkins_url = 'url'
    server = jenkins.Jenkins(jenkins_url, username=jenkins_username, password=jenkins_password)
    return server

def get_building_job( server ):
    # Get job details of each job that is running on the Jenkins instance
    result = None
    jobs = server.get_jobs()
    n_branches = len(jobs)
    for job in jobs:
        color = job["color"]
        if "anime" in color:  
            result = job
            break

    return result

def get_job_details( server, job, t ):
    finished_job = False
    result = None
    print( "Building " + job["name"] + "..." )
    while not finished_job:
        time.sleep( t )
        next_build = server.next_build_number = server.get_job_info(job["name"])['nextBuildNumber']
        job_details = server.get_build_info( job["name"], next_build - 1 )
        # try:
        #     print( job_details["building"] )
        #     print( job_details["result"] )
        #     # print( job_details )
        #     # print( job_details["actions"][0]["causes"][0]["userName"] )
        #     # print( job_details["changeSets"][0]["items"][0]["authorEmail"] )
        # except:
        #     print( "Email user error" )

        if job_details["building"] == False:
            result = job_details["result"]
            finished_job = True

    return result

def publish_result( client, result ):
    print( "Completed: " + result )
    try:
        client.connect( "localhost" )
        client.publish( "jenkins", result )
        print( "Published\n" )
    except:
        print( "Publication error\n" )


def main():
    t = 10
    client = mqtt.Client( "jenkins" )
    server = get_server_instance()

    while True:
        time.sleep( t )
        job = get_building_job( server )
        if job:
            result = get_job_details( server, job, t )
            publish_result( client, result )
            job = None

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