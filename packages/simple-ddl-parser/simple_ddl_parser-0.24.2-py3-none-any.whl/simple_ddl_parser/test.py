from simple_ddl_parser import DDLParser

ddl =  """create table INITIALLY (col1 int);

create table foo.[index] (col1 int);

create table foo.index (col1 int);
    """
result = DDLParser(ddl).run(group_by_type=True, output_mode="hql")

import pprint

pprint.pprint(result)
