from variable import Variable
from arg_manager import ArgManager as AM
from reader.active_record_reader import ActiveRecordReader
from writer.sql_writer import SQLWriter
from node.node_factory import NodeFactory
from configuration_manager import ConfigurationManager
from schema_manager import SchemaManager as sam
from generator_manager import GeneratorManager 


target_genspec = "locus"

pref_manager = ConfigurationManager()
pref_manager.load_genspec(target_genspec)
pref_manager.save_config()

schema_path = pref_manager.data["source"]

schema_manager = sam(NodeFactory.process_schema(ActiveRecordReader.read(schema_path)))
generator_manager = GeneratorManager(pref_manager.get_generator_preload_paths(), pref_manager.data["_cache"])
print "JENNY.py V2"
print ""

pref_manager.save_genspec("",schema_manager.load_preferences(pref_manager.get_current_gemspec(),generator_manager))

pref_manager.save_cached_colls(generator_manager.get_resource_pool())
print ""
print ""
out = pref_manager.data["destination"]
#Import preference, write out diff between prefs and actual schema.


print "Writing 10 Entries in sql"
data_writer = SQLWriter(out,pref_manager.data["sql"])
data_writer.write(schema_manager.current_schema,10)


