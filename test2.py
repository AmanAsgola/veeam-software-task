import os
import time
import logging
import argparse
import shutil

# Parse the command line arguments
parser = argparse.ArgumentParser(description="A program that synchronizes two folders: source and replica.")
parser.add_argument("source", help="The path of the source folder")
parser.add_argument("replica", help="The path of the replica folder")
parser.add_argument("interval", type=int, help="The synchronization interval in seconds")
parser.add_argument("logfile", help="The path of the log file")
args = parser.parse_args()

# Set up the logging configuration
logging.basicConfig(filename=args.logfile, level=logging.INFO, format="%(asctime)s - %(message)s")

def sync_folders(source,replica):
	#listing all the directory in source and replica
	source_items=os.listdir(source)
	replica_items=os.listdir(replica)
	for item in source_items:
		source_path=os.path.join(source,item)
		replica_path=os.path.join(replica,item)
		if os.path.isfile(source_path):
			#file creating operation
			if item not in replica_items:
				shutil.copy2(source_path, replica_path)
				logging.info(f"created file {replica_path}")
				print(f"created file {replica_path}")
			else:
				#file updating operation
				source_mtime=os.path.getmtime(source_path)
				replica_mtime=os.path.getmtime(replica_path)
				if source_mtime>replica_mtime:
					shutil.copy2(source_path, replica_path)
					logging.info(f"updated file {replica_path}")
					print(f"updated file {replica_path}")
		elif os.path.isdir(source_path):
			#folder creating operation
			if item not in replica_items:
				os.mkdir(replica_path)
				logging.info(f"created folder {replica_path}")
				print(f"created folder{replica_path}")
			sync_folders(source_path, replica_path)
	for item in replica_items:
		source_path=os.path.join(source,item)
		replica_path=os.path.join(replica,item)
		if item not in source_items:
			#removing operaion
			if os.path.isfile(replica_path):
				os.remove(replica_path)
				logging.info(f"removed file {replica_path}")
				print (f"removed file {replica_path}")
			#folder removing operation
			elif os.path.isdir(replica_path):
				shutil.rmtree(replica_path)
				logging.info(f"removed folder {replica_path}")
				print(f"folder remove {replica_path}")


# Run an infinite loop
while True:
	try:
	    # Synchronize the folders
	    sync_folders(args.source, args.replica)
	    # Wait for the interval
	    time.sleep(args.interval)
	except KeyboardInterrupt:
		# Print a message when exiting
		print("Exiting program")
		break
