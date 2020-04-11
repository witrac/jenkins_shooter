import time
import multiprocessing
import argparse
import logging

from jenkinsapi.jenkins import Jenkins
import jenkinsapi.api
import RPi.GPIO as GPIO

from shooter_controller import ShooterController

logging.basicConfig(level=logging.DEBUG)

GPIO.setmode(GPIO.BCM)

green_led = 4
red_led = 17
GPIO.setup(green_led, GPIO.OUT)
GPIO.setup(red_led, GPIO.OUT)

controller = ShooterController()

jenkins_username = None
jenkins_password = None

def get_server_instance():
    jenkins_url = 'jenkins_url'
    server = jenkinsapi.api.get_latest_build(jenkins_url, "master", username=jenkins_username, password=jenkins_password, ssl_verify=False)
    print(server)
    return server


def get_job_details():
    """Get job details of each job that is running on the Jenkins instance"""
    # Refer Example #1 for definition of function 'get_server_instance'
    server = get_server_instance()
    if server.is_running():
        return "running"
    if server.is_good():
        return "good"

    return "fail"

    # for job_name, job_instance in server.get_jobs():
    #     print ('Job Name:%s' % (job_instance.name))
    #     print ('Job Description:%s' % (job_instance.get_description()))
    #     print ('Is Job running:%s' % (job_instance.is_running()))
    #     print ('Is Job enabled:%s' % (job_instance.is_enabled()))

def blink():
    while True:
        GPIO.output(green_led, GPIO.LOW)
        GPIO.output(red_led, GPIO.HIGH)
        time.sleep(0.5)
        GPIO.output(green_led, GPIO.HIGH)
        GPIO.output(red_led, GPIO.LOW)
        time.sleep(0.5)
        print("blink...")

def green():
    GPIO.output(green_led, GPIO.HIGH)
    GPIO.output(red_led, GPIO.LOW)

def red():
    GPIO.output(green_led, GPIO.LOW)
    GPIO.output(red_led, GPIO.HIGH)


def main():
    p = multiprocessing.Process(target=blink)
    t = 30
    # This variable controls a one-off shoot after a failure, we could
    # implement a nicer FSM at some point
    last_failure_user = None
    while True:
        result = get_job_details()
        print(result)
        if result == "running" and p.is_alive() == False:
            p = multiprocessing.Process(target=blink)
            p.start()
            t = 10
        elif result == "good":
            if p.is_alive():
                p.terminate()
            green()
            t = 30
        elif result == "fail":
            if p.is_alive():
                p.terminate()
            red()
            # TODO: get the user to shoot from get_job_details()
            last_failure_user = "bob"
            t = 30
        else:
            print("Compilando...")

        if last_failure_user is not None:
            last_failure_user = None
            controller.shoot(last_failure_user)
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
