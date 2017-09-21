# Import statements: the list of outside modules you'll be using in your
# skills, whether from other files in mycroft-core or from external libraries
from os.path import dirname

from adapt.intent import IntentBuilder
from mycroft.skills.core import MycroftSkill, intent_handler
from mycroft.skills.context import adds_context, removes_context
from mycroft.util.log import getLogger
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





# The "create_skill()" method is used to create an instance of the skill.
# Note that it's outside the class itself.
def create_skill():
    return BasicHelpSkill()

