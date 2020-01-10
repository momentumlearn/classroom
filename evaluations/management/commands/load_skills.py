from django.core.management.base import BaseCommand
import re
import os
from pprint import pprint
from evaluations.models import Skill


class Command(BaseCommand):
    help = "Load skills from a file."

    def add_arguments(self, parser):
        parser.add_argument('filename')

    def handle(self, *args, **options):
        filename = options['filename']
        if not os.path.exists(filename):
            print(f"{filename} does not exist!")
            exit(1)
        if not os.path.isfile(filename):
            print(f"{filename} is not a file!")
            exit(1)

        skills = []
        current_skill = None
        with open(filename) as file:
            for line in file.readlines():
                line = line.strip()

                if line == "":
                    continue

                if line.startswith("###"):
                    if current_skill:
                        skills.append(current_skill)

                    current_skill = {
                        "name": line[4:],
                        "levels": [],
                    }

                if current_skill:
                    if re.match(r"^\d\.", line):
                        current_skill['levels'].append(line[3:])
                    elif line.startswith("(") and line.endswith(")"):
                        current_skill['description'] = line[1:-1]

        if current_skill:
            skills.append(current_skill)

        if skills:
            Skill.objects.all().delete()
            for skill_def in skills:
                skill = Skill(name=skill_def['name'],
                              levels=skill_def['levels'])
                if 'description' in skill_def:
                    skill.description = skill_def['description']
                skill.save()
        print(f"{len(skills)} skills loaded.")
