from variable import Variable
from reader.active_record_reader import ActiveRecordReader
from reader.sql_reader import SQLReader
from writer.sql_writer import SQLWriter
from node.node_factory import NodeFactory
from configuration_manager import ConfigurationManager
from schema_manager import SchemaManager as sam
from generator_manager import GeneratorManager 


target_genspec = "wordy"

pref_manager = ConfigurationManager()
pref_manager.load_genspec(target_genspec)
pref_manager.save_config()

schema_path = pref_manager.data["source"]
schema_type = schema_path.split(".")[-1].strip()
if(schema_type == "sql"):
	schema_path = SQLReader.read(schema_path)
else:
	schema_path = ActiveRecordReader.read(schema_path)
schema_manager = sam(NodeFactory.process_schema(schema_path))
generator_manager = GeneratorManager(pref_manager.get_generator_preload_paths(), pref_manager.data["_cache"])
print "JENNY.py V2"
print ""

pref_manager.save_genspec("",schema_manager.load_preferences(pref_manager.get_current_gemspec(),generator_manager))

pref_manager.save_cached_colls(generator_manager.get_resource_pool())
print ""
print ""
out = pref_manager.data["destination"]
#Import preference, write out diff between prefs and actual schema.


print "Writing 10 Entries in sql to " + out
data_writer = SQLWriter(out,pref_manager.data["sql"])
data_writer.write(schema_manager.current_schema,10)


