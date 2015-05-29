import sys
import json
from cmd3.console import Console
from cloudmesh_database.dbconn import get_mongo_db, DBConnFactory

from cloudmesh_management.base_project import Project
from base_committee import Committee
from base_review import Review
from project import Projects
from user import User
from bson.objectid import ObjectId
from tabulate import tabulate
from util import requires_roles
from cloudmesh_management.mongo import Mongo
from cloudmesh_base.util import banner


class Committees(object):

    def __init__(self):
        obj = Mongo()
        obj.check_mongo()
        get_mongo_db("manage", DBConnFactory.TYPE_MONGOENGINE)

    @classmethod
    @requires_roles('admin', 'reviewer')
    def setup_committee(cls):
        try:
            user = User.objects(username="super").first()
            count = Committee.objects.count()
            print count
            if count > 0:
                Console.error("Committee has already been setup.")
                return
            data = Committee(
                reviewers=[user],
                reviews=[]
            )
            data.save()
            Console.info("Committee setup successful.")
        except:
            print sys.exc_info()
            Console.error("Committee setup failed.")


    @classmethod
    @requires_roles('admin', 'reviewer')
    def add_reviewer(cls, username):
        if username:
            try:
                user = User.objects(username=username).first()
                if user:
                    try:
                        found = Committee.objects(reviewers__contains=user)
                        if not found:
                            Committee.objects().update_one(push__reviewers=user)
                            User.objects(username=username).update_one(push__roles="reviewer")
                            Console.info("User {0} added as Reviewer.".format(username))
                        else:
                            Console.error("User {0} already exists as a reviewer.".format(username))
                    except:
                        print sys.exc_info()
                        Console.info("Reviewer {0} addition failed.".format(username))
                else:
                    Console.error("Please specify a valid user")
            except:
                print sys.exc_info()
                Console.error("Oops! Something went wrong while trying to add project reviewer")
        else:
            Console.error("Please specify a reviewer name to be added.")
        pass

    @classmethod
    @requires_roles('admin', 'reviewer')
    def remove_reviewer(cls, username):
        if username:
            try:
                user = User.objects(username=username).first()
                if user:
                    try:
                        found = Committee.objects(reviewers__contains=user)
                        if found:
                            Committee.objects().update_one(pull__reviewers=user)
                            User.objects(username=username).update_one(pull__roles="reviewer")
                            Console.info("User `{0}` removed as Reviewer.".format(username))
                        else:
                            Console.error("Please specify a valid user name.")
                    except:
                        Console.info("Reviewer {0} removal failed.".format(username))
                else:
                    Console.error("Please specify a valid user")
            except:
                Console.error("Oops! Something went wrong while trying to remove reviewer")
        else:
            Console.error("Please specify a reviewer name to be removed.")
        pass

    @classmethod
    @requires_roles('admin', 'reviewer')
    def add_review(cls, project_id, username, review):
        if review:
            review = Review.objects(project_id=project_id).first()
            review_text = username+" - "+review
            Review.objects().update_one(push__reviews=review_text)
        else:
            Console.error("Please provide a review text.")
        pass

    @classmethod
    @requires_roles('reviewer')
    def approve_project(cls, project_id=None, text=None):
        if project_id and text:
            current_status = Projects.get_project_status(project_id)
            if current_status != "active":
                Projects.amend_project_status(project_id, "active")
                cls.add_review(project_id, "user", text)
        else:
            Console.error("Please specify a project id to be approved and a message.")
        pass

    @classmethod
    @requires_roles('admin', 'reviewer')
    def list_committee(cls, project_id=None):
        if project_id is None:
            req_fields = ["reviewers"]
            committee_json = Committee.objects.only(*req_fields).to_json()
            committee_dict = json.loads(committee_json)
            if committee_dict:
                cls.display(committee_dict)
            else:
                Console.info("No committees found in the database.")
        pass


    @classmethod
    @requires_roles('admin', 'reviewer')
    def display(cls, committee_dict=None):
        if bool(committee_dict):
            values = []
            for entry in committee_dict:
                items = []
                headers = []
                for key, value in entry.iteritems():
                    if key == "project_id":
                        entry = ""
                        if value:
                            items.append(value)
                            headers.append("Project ID")
                            project = Project.objects(project_id=value).first()
                            entry += project.title
                            # for item in value:
                            #     project = Project.objects.get(id=ObjectId(item.get('$oid')))
                            #     entry += project.title
                            # entry = entry.strip(',')
                            items.append(entry)
                            headers.append("Project Name")
                    elif key == "reviewers":
                        entry = ""
                        if value:
                            for item in value:
                                user = User.objects.get(id=ObjectId(item.get('$oid')))
                                if user.username != "super":
                                    entry += user.firstname + " " + user.lastname + ", "
                            entry = entry.strip(', ')
                            if entry:
                                items.append(entry)
                            else:
                                items.append("No reviewers yet.")
                        else:
                            items.append("No reviewers yet.")
                        headers.append(key.replace('_', ' ').title())
                values.append(items)

            # Re-order the columns as per our requirement
            # header order 1, 2, 0 => project name, project_id, reviewers
            header_order = [0]
            headers = [headers[i] for i in header_order]
            new_values = [[x[0]] for x in values]
            table_fmt = "fancy_grid"
            table = tabulate(new_values, headers, table_fmt)
            separator = ''
            try:
                seperator = table.split("\n")[1].replace("|", "+")
            except:
                separator = "-" * 50
            print separator
            print table
            print separator
        else:
            Console.error("No Committees to display.")


def main():
    committee = Committees()
    # committee.setup_committee()
    # committee.add_reviewer('donny')
    committee.list_committee()


if __name__ == "__main__":
    main()
