# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft.util.log import getLogger
import sh
import pexpect
import requests
import json
import datetime
__author__ = 'brihopki'

# Logger: used for debug lines, like "LOGGER.debug(xyz)". These
# statements will show up in the command line when running Mycroft.
LOGGER = getLogger(__name__)



# The logic of each skill is contained within its own class, which inherits
# base methods from the MycroftSkill class with the syntax you can see below:
# "class ____Skill(MycroftSkill)"
class BasicHelpSkill(MycroftSkill):

    # The constructor of the skill, which calls MycroftSkill's constructor
    def __init__(self):
        super(BasicHelpSkill, self).__init__(name="BasicHelpSkill")

    @intent_handler(IntentBuilder('InstallIntent').require('platform').require('install'))
    def handle_install_mycroft(self, message):
        platform = message.data.get('platform')
        if platform == 'source' or platform == 'git':
            self.speak('You can install from {} via the instructions at '
                       'https://docs.mycroft.ai/development/installation'
                       '/git.clone.install'.format(platform))

        elif platform == 'pi' or  platform == 'picroft':
            self.speak('You can install from {} via the instructions at '
                       'https://docs.mycroft.ai/development/installation'
                       '/raspberry.pi'.format(platform))
        elif platform == 'docker':
            self.speak('You can find instructions for {} install at '
                       'https://github.com/MycroftAI/docker-mycroft'
                       .format(platform))
        elif platform == 'plasmoid':
            self.speak('Follow the plasmoid install guide at, '
                       'https://cgit.kde.org/plasma-mycroft.git/'
                       'tree/Readme.md  If you are running an Ubuntu '
                       'or Fedora based distro you can find the install '
                       'scripts here, https://github.com/MycroftAI/installers')
        elif platform == 'qtapp' or platform == 'qtapplication':
            self.speak('Appimage for the standalone Qtapplication is available at '
                       'https://github.com/AIIX/Mycroft-Ai-QtApplication/releases')

    @intent_handler(IntentBuilder('DocIntent').optionally('platform').require('doc'))
    def handle_docs_mycroft(self, message):
        platform = message.data.get('platform')
        if platform:
            if platform == 'picroft' or platform == 'pi':
                self.speak('You can find the picroft wiki at '
                           'https://github.com/MycroftAI/'
                           'enclosure-picroft/wiki')
        else:
            self.speak('You can find the general docs at https://docs.mycroft.ai')

    @intent_handler(IntentBuilder('TsIntent').optionally('platform').require('ts'))
    def handle_ts_mycroft(self, message):
        platform = message.data.get('platform')
        if not platform:
            self.speak('General troubleshooting information can be found at '
                       'https://docs.mycroft.ai/development/faq or '
                       'channel ~troubleshooting')
        if platform:
            if platform == 'plasmoid':
                output = "Steps to troubleshoot your plasmoid install:\n " \
                         "1. Check if mycroft is installed correctly\n " \
                         "2. Open plasmoid settings and check your mycroft path\n " \
                         "3. Run plasmashell in debug mode report error messages\n " \
                         "4. Submit your issue's on the ~desktop channel, or\n " \
                         "5. Create a bug report at https://bugs.kde.org\n " \
                         "/describecomponents.cgi?product=plasma-mycroft"
                self.speak(output)

    @intent_handler(IntentBuilder('Skills').optionally('action').require('skills'))
    def handle_skills_mycroft(self, message):
        action = message.data.get('action')
        if action == 'available':
            self.speak('The current list of mycroft skills can be found at, '
                       'https://github.com/MycroftAI/mycroft-skills')

    @intent_handler(IntentBuilder('Settings').optionally('setting_values').require('settings'))
    def handle_skills_mycroft(self, message):
        setting = message.data.get('setting_values')
        if setting == 'wake' or setting == 'wake word':
            self.speak('You can adjust the wake word and sensitivity of mycroft '
                       'by using the instructions at, '
                       'https://docs.mycroft.ai/development/faq')

    @intent_handler(IntentBuilder('Logs').require('log'))
    def handle_log_mycroft(self, message):

        tail = pexpect.run("tail -30 /var/log/mycroft-skills.log")
        self.speak("``` {} ```".format(tail))

    @intent_handler(IntentBuilder('Services').require('services'))
    def handle_log_mycroft(self, message):
        self.speak("Restarting services")
        pexpect.run('./opt/mycroft/skills/mycroft-skill-basichelp/restart.sh')


# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return BasicHelpSkill()

