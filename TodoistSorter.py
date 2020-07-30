import datetime
import sqlite3
import uuid

import requests
from todoist.api import TodoistAPI


class Sorter:
    def __init__(self, api_token, project_id):
        self.token = api_token
        self.api = TodoistAPI(api_token)
        self.api.sync()

        self.project_id = project_id
        self.dbfilename = 'Todoist.db'
        self.dbtableprefix = 'Sections_'
        self.dbtablename = self.dbtableprefix + str(project_id)

    def initialize_db(self):
        conn = sqlite3.connect(self.dbfilename)
        db = conn.cursor()
        query = 'CREATE TABLE IF NOT EXISTS "{}" ("item_project" INT, "item_content" TEXT, "item_section" INT, "last_updated" TEXT)'.format(self.dbtablename)
        db.execute(query)
        db.close()

    def get_section_name(self, section_id):
        sectionList = self.api.state['sections']
        for section in sectionList:
            if section['id'] == section_id:
                return section['name']
        # RETURN FALSE IF NO MATCH IS FOUND
        return False

    def capitalize_item(self, item_id):
        item_content = self.api.items.get_by_id(item_id)['content']
        if not item_content[0].isupper():
            new_content = item_content[0].upper() + item_content[1:]

            # WRITE UPDATED CONTENT TO TODOIST
            item = self.api.items.get_by_id(item_id)
            item.update(content=new_content)
            self.api.commit()

    def get_historic_section(self, item_id):
        item = self.api.items.get_by_id(item_id)

        self.initialize_db()
        conn = sqlite3.connect(self.dbfilename)
        selectQuery = "SELECT item_content, item_section FROM {} WHERE item_content = '{}' LIMIT 1".format(self.dbtablename, item['content'].lower())
        db = conn.cursor()
        result = db.execute(selectQuery).fetchone()
        db.close()
        conn.commit()
        if result is not None:
            return result[1]
        else:
            return None

    def learn(self):
        self.initialize_db()
        conn = sqlite3.connect(self.dbfilename)
        query = ""

        itemList = self.api.state['items']
        for item in itemList:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")  # USED TO INSERT INTO DB WHEN UPDATING
            if item['project_id'] == self.project_id and item['section_id'] is not None:

                # GET HISTORIC SECTION
                historic_section = self.get_historic_section(item['id'])
                if historic_section == item['section_id']:  # NO UPDATE NEEDED
                    pass

                if historic_section is None:  # ADD ITEM TO DB
                    query = "INSERT INTO {} (item_project, item_content, item_section, last_updated) VALUES ({},'{}',{}, '{}')".format(self.dbtablename, item['project_id'], item['content'].lower(),
                                                                                                                                   item['section_id'], timestamp)

                if historic_section is not None and historic_section != item['section_id']:  # UPDATE CURRENT SECTION
                    query = "UPDATE {} SET item_section = {}, last_updated = '{}' WHERE item_content = '{}'".format(self.dbtablename, item['section_id'], timestamp, item['content'].lower())

                db = conn.cursor()
                db.execute(query)
                db.close()
                query = ""

        conn.commit()

    # def adjust_item_section_UNSUPPORTED(self, item_id):
    #     # TODO WRITE UPDATED CONTENT TO TODOIST
    #     if self.get_historic_section(item_id) is not None:
    #         item = self.api.items.get_by_id(item_id)
    #         item.move(parent_id=item_id)
    #         self.api.commit()

    def adjust_item_section(self, item_id):
        # USING MANUAL REQUESTS METHOD AS SECTIONS ARENT SUPPORTED IN CURRENT VERSION OF TODOIST SYNC API-LIBRARY
        state = uuid.uuid4()
        apiUrlSync = "https://api.todoist.com/sync/v8/sync"
        commands = '[{"type": "item_move", "uuid": "' + str(state) + '", "args": {"id": ' + str(item_id) + ', "section_id": ' + str(self.get_historic_section(item_id)) + '}}]'

        payload = {"token": str(self.token), 'commands': commands}
        requests.post(apiUrlSync, data=payload).json()
