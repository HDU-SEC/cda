import subprocess
import csv
import os

tmp_query_path = "./codeql-custom-queries-cpp/tmpquery.ql"
path_query_path = "./codeql-custom-queries-cpp/pathquery.ql"
target_query_path = "./codeql-custom-queries-cpp/gadget-search.ql"
database_path = "./codeql_db"
output_path = "./output/result.bqrs"
bh_query_path = "./codeql-custom-queries-cpp/bh-search.ql"
mmio_query_path = "./codeql-custom-queries-cpp/mmio-search.ql"
# startFunction = "ehci_work_bh"
# targetFunction = "dma_memory_read"

#get all entry function 
#get all bh entry function
#executing the query
result = subprocess.run(["codeql", "query", "run","--database",database_path,bh_query_path,"--output",output_path])
bh_list = []
#parsing the result to csv format
subprocess.run("codeql bqrs decode --output output/result.csv -- output/result.bqrs")
filename = ".//output/result.csv"
with open(filename, 'r') as csvfile:
   csvreader = csv.reader(csvfile)
   for _ in range(2):
      next(csvreader)
   for row in csvreader:
      row[0] = row[0].strip('|')
      row[0] = row[0].strip()
      bh_list.append(row[0])
#print(bh_list)

#get all mmio entry function
#executing the query
result = subprocess.run(["codeql", "query", "run","--database",database_path,mmio_query_path,"--output",output_path])
mmio_list = []
#parsing the result to csv format
subprocess.run("codeql bqrs decode --output output/result.csv -- output/result.bqrs")
filename = ".//output/result.csv"
with open(filename, 'r') as csvfile:
   csvreader = csv.reader(csvfile)
   for _ in range(2):
      next(csvreader)
   for row in csvreader:
      row[0] = row[0].strip('|')
      row[0] = row[0].strip()
      mmio_list.append(row[0])
#print(mmio_list)

#set the target function list
target_list = ['dma_memory_map', 'dma_memory_unmap', 'dma_memory_write', 'dma_memory_read']

tmpNode = []
allNode = []
tmpPath = []

edge = [[0] * 100 for _ in range(100)]


def changeFile(filePath, startFun, targetFun):
   file_path = filePath
   startFun_line_number = 12
   targetFun_line_number = 17
# read the file and modify the specific lines
   with open(file_path, 'r', encoding='utf-8') as f:
      lines = f.readlines()
      lines[startFun_line_number] = '  func.getName() = "' + startFun + '"\n'
      lines[targetFun_line_number] = ' func.getName() = "' + targetFun + '"\n'

# write back to the file
   with open(file_path, 'w', encoding='utf-8') as f:
      f.writelines(lines)


#changeFile(path_query_path, mmio_list[0], bh_list[0])

def getPathFun(A, B):
   changeFile(path_query_path, A, B)
   result = subprocess.run(["codeql", "query", "run","--database",database_path,path_query_path,"--output",output_path])
##make the result to csv format
   subprocess.run("codeql bqrs decode --output output/result.csv -- output/result.bqrs")
   filename = "./output/result.csv"
##load the csv file and get the data
   candidate = []
##read the csv file and get the data
   with open(filename, 'r') as csvfile:
      csvreader = csv.reader(csvfile)
      for _ in range(2):
         next(csvreader)
      for row in csvreader:
         row[0] = row[0].strip('|')
         row[0] = row[0].strip()
         candidate.append(row[0])
      #print(row[0])
      #print(candidate)
      return candidate

#get all the function that may be called in the path from A to B
def getTmpFun(A, B):
   changeFile(tmp_query_path, A, B)
   result = subprocess.run(["codeql", "query", "run","--database",database_path,tmp_query_path,"--output",output_path])
##make the result to csv format
   subprocess.run("codeql bqrs decode --output output/result.csv -- output/result.bqrs")
   filename = "./output/result.csv"
##store all the intermediate function calls
   candidate = []
##read the csv file and get the data
   with open(filename, 'r') as csvfile:
      csvreader = csv.reader(csvfile)
      for _ in range(2):
         next(csvreader)
      for row in csvreader:
         row[0] = row[0].strip('|')
         row[0] = row[0].strip()
         candidate.append(row[0])
      #print(row[0])
      #print(candidate)
      return candidate

#DFS algorithm to find all paths from A to B 
def dfs(current_node, end, path, visited, all_paths):
   path.append(current_node)
   visited.add(current_node)

   if current_node == end:
      all_paths.append(path.copy())
      #print(path)
   else:
      for node in tmpNode:
         index_a = allNode.index(current_node)
         index_b = allNode.index(node)
         if node not in visited and edge[index_a][index_b]:
            dfs(node, end, path, visited, all_paths)

   path.pop()
   visited.remove(current_node)

def find_all_paths(nodes, start, end):
    nodes.append(end)
    all_paths = []
    dfs(start, end, [], set(), all_paths)
    return all_paths

sel_num = 0
# startFunction = 'virtio_gpu_cursor_bh'
# targetFunction = 'dma_memory_map'
#alternatively, you can use the bh_list and mmio_list to get all the entry functions and target functions, and then find all the paths between them
for startFunction in mmio_list:
   for targetFunction in target_list:
      edge = [[0] * 100 for _ in range(100)]
      tmpNode = []
      allNode = []
      tmpPath = []
      all_paths = []
      #get information of Node
      tmpNode = getTmpFun(startFunction, targetFunction)
      if not tmpNode:
         continue
      for node in tmpNode:
         allNode.append(node)
      allNode.append(startFunction)
      allNode.append(targetFunction)
      #print(len(allNode))

      #get Path information
      tmpPath = getPathFun(startFunction, targetFunction)
      for path in tmpPath:
         parts = path.split("->")
         node1 = parts[0].strip()
         node2 = parts[1].strip()
         #print(node1)
         #print(node2)
         index_a = allNode.index(node1)
         index_b = allNode.index(node2)
         #print(index_a)
         #print(index_b)
         edge[index_a][index_b] = 1

      all_paths = find_all_paths(tmpNode, startFunction, targetFunction)
      print('gadget from ' + startFunction + ' to ' + targetFunction)
      print('gadgetnum is : %d' %(len(all_paths)))
      #print(len(all_paths))
      with open("./output/mmio.txt", "a", encoding="utf-8") as f:
         for path in all_paths:
            #print(sel_num + ':')
            print("path %d ：" % (sel_num))
            print(" -> ".join(path))
            f.write("path %d ：\n" % sel_num)
            f.write(" -> ".join(path) + "\n\n")
            sel_num = sel_num + 1