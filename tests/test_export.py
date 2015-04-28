from cloudmesh_management.dbutil import DBUtil
from cloudmesh_base.util import HEADING


class ExportTest:
    def setup(self):
        # HEADING()
        pass

    def teardown(self):
        # HEADING()
        pass

    def test_export(self):
        HEADING()
        obj = DBUtil()
        obj.serialize(db="cloudmesh", collection="cloudmesh")





