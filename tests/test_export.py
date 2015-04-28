from cloudmesh_management.dbutil import DBUtil
from cloudmesh_base.util import HEADING


class ExportTest:
    def setup(self):
        # HEADING()
        pass

    def teardown(self):
        # HEADING()
        pass

    def test_generate(self):
        HEADING()
        print "Running dbutil Test"
        database = "cloudmesh"
        dbutil = DBUtil()
        dbutil._connect(db=database)




