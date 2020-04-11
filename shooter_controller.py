import time
import logging
import RPi.GPIO

logger = logging.getLogger("jenkins_shooter")

# Map defining the relation between users and required steps
USER_TO_STEPS = {"bob": 12, "alice": 20}

# Map defining the RPi pinout connecting the stepper
PINOUT = {
    "stepper_enable": 22,
    "stepper_direction": 21,
    "stepper_step": 20,
    "shooter_trigger": 0xFF,  # TODO: Set here the pin(s) for the actual shooting
}


class ShooterController:
    """This class controls the shooter

    On the one hand, uses a stepper connected to the RPi to move the toy gun
    to point to an engineer. On the other hand, uses a [TODO: what?] to trigger
    the toy gun and alert the engineer.
    An enginner is pointed with a fixed number of steps, moving the toy only
    horizontally
    """

    def __init__(self):
        RPi.GPIO.setmode(RPi.GPIO.BCM)
        RPi.GPIO.setup(PINOUT["stepper_enable"], RPi.GPIO.OUT)
        RPi.GPIO.setup(PINOUT["stepper_direction"], RPi.GPIO.OUT)
        RPi.GPIO.setup(PINOUT["stepper_step"], RPi.GPIO.OUT)
        self._stepper_disable()

    def shoot(self, user):
        """Shoot to the given user

        It always assumes it is in the start position. It will step the
        required number of steps for the user, then shoot, then step back
        the same number of steps to go back to the start positoin
        """
        if not user in USER_TO_STEPS.keys():
            logger.error("Unknown user %s" % user)
            return
        logger.info("Shotting to user %s" % user)
        self._stepper_enable()
        self._stepper_forward(USER_TO_STEPS[user])
        # TODO: shot!
        self._stepper_reverse(USER_TO_STEPS[user])
        self._stepper_disable()

    def _stepper_enable(self):
        logger.debug("stepper: enable")
        RPi.GPIO.output(PINOUT["stepper_enable"], False)

    def _stepper_disable(self):
        logger.debug("stepper: disable")
        RPi.GPIO.output(PINOUT["stepper_enable"], True)

    def _stepper_step_once(self):
        logger.debug("stepper: step")
        RPi.GPIO.output(PINOUT["stepper_step"], True)
        time.sleep(0.0005)
        RPi.GPIO.output(PINOUT["stepper_step"], False)
        time.sleep(0.0005)

    def _stepper_forward(self, steps):
        logger.debug("stepper: forward %d steps", steps)
        RPi.GPIO.output(PINOUT["stepper_direction"], True)
        for _ in range(steps):
            self._stepper_step_once()

    def _stepper_reverse(self, steps):
        logger.debug("stepper: reverse %d steps", steps)
        RPi.GPIO.output(PINOUT["stepper_direction"], False)
        for _ in range(steps):
            self._stepper_step_once()
