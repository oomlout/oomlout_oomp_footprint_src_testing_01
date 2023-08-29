import os
import yaml
import shutil
import oom_base


github_repo_details = {}

def make_footprint_yaml():
    #print what's happening
    print('Making footprint yaml')
    repos = []
    kitespace_meaglist_dir = rf'C:\GH\kitspace\kicad_footprints'
    for dir in os.listdir(kitespace_meaglist_dir):
        #ignore if .git or ,github
        if dir != '.git' and dir != '.github':
            if os.path.isdir(os.path.join(kitespace_meaglist_dir, dir)):
                #go through each directory in dir
                for f in os.listdir(os.path.join(kitespace_meaglist_dir, dir)):
                    #if .pretty
                    repo = {}
                    repo['name'] = f
                    repo['owner'] = dir
                    repo['url'] = f'http://github.com/{dir}/{f}'
                    repos.append(repo)
    #dump repos to repos.yaml
    with open('repos.yaml', 'w') as f:
        yaml.dump(repos, f)


def clone_and_copy_footprints():
    #load footprint repros from repros.yaml
    repos = []  
    with open('repos.yaml', 'r') as f:
        repos += yaml.load(f, Loader=yaml.FullLoader)
    with open('repos_manual.yaml', 'r') as f:
        repos += yaml.load(f, Loader=yaml.FullLoader)
    
    #go through each repo
    for repo in repos:
        owner = repo['owner']
        name = repo['name']
        #print what's happening
        print(f'Cloning {repo["name"]} from {repo["url"]} and copying footprints')
        #clone repo into tmp/repo
        os.system(f'git clone {repo["url"]} tmp/{repo["name"]}')
        #get a list of all the files in tmp/repo that end in kicad_mod
        kicad_mods = []
        #recursively go through all directories in tmp/repo
        
        for root, dirs, files in os.walk(f'tmp/{repo["name"]}'):
            #go through each file
            for file in files:
                #if it ends in kicad_mod
                #https://github.com/1Bitsy/1bitsy-hardware-lib/blob/master/kicad/1bitsy.pretty/1bitsy-basic-sl-1xx-xx-19.kicad_mod
                if file.endswith('kicad_mod'):
                    #add full path to kicad_mods                    
                    kicad_mod = {}
                    file_full = os.path.join(root, file)
                    #replace \\ with /
                    file_full = file_full.replace('\\', '/')

                    



                    kicad_mod['file'] = file_full
                    kicad_mod['name'] = name
                    #https://github.com/1Bitsy/1bitsy-hardware-lib/blob/master/kicad/1bitsy.pretty/1bitsy-basic-sl-1xx-xx-19.kicad_mod
                    #remove tmp/repo from file_full
                    file_full = file_full.replace(f'tmp/{name}/', '')
                    kicad_mod['github_path'] = f'http://github.com/{owner}/{name}/blob/master/{file_full}'
                    kicad_mods.append(kicad_mod)
        

        #call make base_owner_footprint_library
        footprints = kicad_mods
        make_base_owner_footprint_library(repo=repo, footprints=footprints, kicad_mod=kicad_mod)



        
        
        
        
        #remove repo using os.system
        ##windows_name = repo["name"].replace('/', '\\')
        ##os.system(rf'rmdir /s /q tmp\{windows_name}')
        
        
        
        pass
    
### make a folder thart has all the footprints in it
def make_base_owner_footprint_library(**kwargs):
    repo = kwargs['repo']
    footprints = kwargs['footprints']
    owner = repo['owner']
    name = repo['name']
    kicad_mod = kwargs['kicad_mod']
    owner_footprint_library_directory = f'footprint_library_owner/{owner}_{name}'
    #if it doesn't exist make it with all needed subfolders
    #if not os.path.exists(owner_footprint_library_directory):
        #make with all needed subfodlers
    #    os.makedirs(owner_footprint_library_directory)
        



    #copy all the footprints into it not using shutil
    for footprint in footprints:
        #us shutil
        file = footprint['file']
        #just the filename from the full path
        filename = os.path.basename(file)
    #try:
        ##no longer done
        ##shutil.copyfile(file, f'footprint_library_owner/{owner}_{name}/{filename}') 

        ####### get filename details
        file_full = file
        #LIBRARY IS THE FOLDER THAT HAS .PRETTY IN IT
        #get the library name from the path
        split = file_full.split('/')
        #get the index of .pretty
        count = 0
        for s in split:
            count += 1
            if '.pretty' in s:
                break
            
        #get the library name
        library = split[count-1]
        library = library.replace('.pretty', '')
        #footprint name is the one that has kicad_mod in it
        count = 0
        for s in split:
            count += 1
            if 'kicad_mod' in s:
                break
            
        #get the footprint name
        footprint_name= split[count-1]
        footprint_name = footprint_name.replace('.kicad_mod', '')


        ###### footprints_folder

        """
        #copy the footprint into footprints/owner/name/footprint_name/working.kicad_mod
        just_filename = os.path.basename(file)
        folder = f'footprints_folder/{owner}/{library}/{footprint_name}/working'
        folder_0 = folder
        file_out= f'{folder}/working.kicad_mod'
        #if the folder doesn't exist make it
        if not os.path.exists(folder):
            os.makedirs(folder)
        #copy the file
        shutil.copyfile(file, file_out)
        """
        

        ###### footprints_flat

        #flat approach
        just_filename = os.path.basename(file)
        folder_flat = f'{owner}_{library}_{footprint_name}'
        #remove all charachters that can't be used in windows fiolenames with _
        #remove kicad_mod
        folder_flat = folder_flat.replace('.kicad_mod', '')
        folder_flat = folder_flat.replace('/', '_')
        folder_flat = folder_flat.replace('\\', '_')
        folder_flat = folder_flat.replace(':', '_')
        folder_flat = folder_flat.replace('*', '_')
        folder_flat = folder_flat.replace('?', '_')
        folder_flat = folder_flat.replace('"', '_')
        folder_flat = folder_flat.replace('<', '_')
        folder_flat = folder_flat.replace('>', '_')
        folder_flat = folder_flat.replace('|', '_')
        folder_flat = folder_flat.replace('-', '_')        
        folder_flat = folder_flat.replace('+', '_')
        folder_flat = folder_flat.replace(' ', '_')
        folder_flat = folder_flat.replace('.', '_')
        folder_flat = folder_flat.replace('__', '_')
        folder_flat = folder_flat.replace('__', '_')
        folder_flat = folder_flat.replace('__', '_')
        folder_flat = folder_flat.replace('__', '_')
        # to lower case
        folder_flat = folder_flat.lower()
        folder = f'footprints_flat/{folder_flat}/working'
        file_out= f'{folder}/working.kicad_mod'
        #if the folder doesn't exist make it
        if not os.path.exists(folder):
            os.makedirs(folder)
        #copy the file
        shutil.copyfile(file, file_out)

        #remove tmp/ from repo file
        footprint['file'] = footprint['file'].replace('tmp/', '')
        #put repo and footprint element into a single dict        
        footprint_details = {}

        for key in repo:
            footprint_details[key] = repo[key]
        for key in footprint:
            footprint_details[key] = footprint[key]
        #add all other variables to footprint_details
        footprint_details['footprint_library_directory'] = owner_footprint_library_directory
        footprint_details['footprint_library_directory_flat'] = folder
        
        #add repo to footprint details
        
        footprint_details['oomp_key'] = f'oomp_{folder_flat}'
        footprint_details['oomp_key_full'] = f'oomp_footprint_{folder_flat}'
        footprint_details['oomp_key_simple'] = f'{folder_flat}'

        #add various useful links to footprint details
        links = {}
        
        repo_url = repo['url']
        repo_full = get_repo_details(repo_url=repo_url)
        footprint_details['repo'] = repo_full
        if len(repo_full) > 2:
            #get the repo url details from github using their api
            html_url = repo_full['html_url']
            github_src = f'{kicad_mod["github_path"]}'
            links['github_src'] = github_src
            links['github_src_repo'] = html_url
            #get owner from html_url
            owner = html_url.split('/')[-2]
            links['github_owner'] = f'{owner}'
            #get repo name from html_url
            repo_name = html_url.split('/')[-1]
            links['github_repo_name'] = f'{repo_name}'
        else:
            ###kicad on gitlab
            html_url = 'https://gitlab.com/kicad/libraries/kicad-footprints'
            github_src = f'{kicad_mod["github_path"]}'
            github_src = github_src.replace('github.com', 'gitlab.com')
            links['github_src'] = github_src
            links['github_src_repo'] = html_url
            #get owner from html_url
            ##owner = html_url.split('/')[-2]
            ##links['github_owner'] = f'{owner}'
            #get repo name from html_url
            ##repo_name = html_url.split('/')[-1]
            ##links['github_repo_name'] = f'{repo_name}'

        #oomp_src flat link
        oomp_src_flat = f'footprints_flat/{folder}'
        links['oomp_src_flat'] = oomp_src_flat
        oomp_src_flat_github = f'https://github.com/oomlout/oomlout_oomp_footprint_src/tree/main/{folder}'
        links['oomp_src_flat_github'] = oomp_src_flat_github
        
        #oomp source folder lnk
        #oomp_src_folder = f'footprints_folder/{folder_0}'
        #links['oomp_src_folder'] = oomp_src_folder
        #oomp_src_folder_github = f'https://github.com/oomlout/oomlout_oomp_footprint_src/tree/main/{folder_0}'
        #links['oomp_src_folder_github'] = oomp_src_folder_github
        
        #oomp_bot link
        oomp_bot_folder = folder.replace("footprints_flat","footprints")
        oomp_bot = f'{oomp_bot_folder}'
        links['oomp_bot'] = oomp_bot
        oomp_bot_github = f'https://github.com/oomlout/oomlout_oomp_footprint_bot/tree/main/{oomp_bot_folder}'
        links['oomp_bot_github'] = oomp_bot_github
        
        #doc folder
        #oomp_doc_folder = folder_0.replace("footprints_folder","footprints")
        #oomp_doc = f'footprints/{oomp_doc_folder}/'
        #links['oomp_doc'] = oomp_doc
        #oomp_doc_github = f'https://github.com/oomlout/oomlout_oomp_footprint_doc/tree/main/footprints/{oomp_doc_folder}'
        #links['oomp_doc_github'] = oomp_doc_github

        

        #add links to footprint details
        footprint_details['links'] = links

        #####adding details to working.yaml
        pass
        #add all the keys from repo to footprint_details
        
        #using kiutils load in working.kicad_mod
        try:
            from kiutils.footprint import Footprint
            footprint2 = Footprint().from_file(f'{folder}/working.kicad_mod')
            footprint_details['footprint'] = get_footprint_details(footprint=footprint2) 
        except Exception as e:
            print(f'error loading {folder}/working.kicad_mod')
            print(e)
            footprint_details['error'] = str(e)
            pass

        import oom_base

        oomp_deets = {}

        
        #add a md5 hash of the id as a keyed item to kwargs
        import hashlib
        md5 = hashlib.md5(folder_flat.encode()).hexdigest() 
        oomp_deets["md5"] = md5
        #trim md5 to 6 and add it as md5_6
        oomp_deets["md5_5"] = md5[0:5]
        #add to md5_5 dict
        md5_6 = md5[0:6]
        oomp_deets["md5_6"] = md5_6
        oomp_deets["md5_10"] = md5[0:10]
        
        oomp_deets['footprint_name'] = oom_base.remove_special_characters(footprint_name).lower()
        oomp_deets['library_name'] = oom_base.remove_special_characters(library).lower()
        oomp_deets['owner_name'] = oom_base.remove_special_characters(owner).lower()
        oomp_deets['original_filename'] = footprint["file"]
        oomp_deets['oomp_key'] = f'oomp_{folder_flat}'
        oomp_deets['oomp_key_extra'] = f'oomp_footprint_{folder_flat}'
        oomp_deets['oomp_key_full'] = f'oomp_footprint_{folder_flat}_{md5_6}'
        oomp_deets['oomp_key_simple'] = f'{folder_flat}'


        footprint_details['oomp'] = oomp_deets
        pass
        #dump to yaml in flat directory
        with open(f'{folder}/working.yaml', 'w') as f:
            yaml.dump([footprint_details], f)
        #dump to yaml in flat directory
        #with open(f'{folder_0}/working.yaml', 'w') as f:
        #    yaml.dump([footprint_details], f)
        #print a progress dot
        print('.', end='', flush=True)
    #except Exception as e:
    #    print(f'error copying {file}')
    #    print(e)
    #    pass



def make_footprints_readme():
    counter = 1
    #folders = ["footprints_flat", "footprints_folder"] ##folder not working at the moment
    folders = ["footprints_flat"]
    for folder in folders:
        #go through all the files in folder 
        for root, dirs, files in os.walk(folder):
            #if its a directory
            if os.path.isdir(root):
                #if it's called working
                if root.endswith('working'):
                    #load the working.yaml file from the folder
                    #try:
                        with open(f'{root}/working.yaml', 'r') as yaml_file:
                            yaml_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)
                        #create a readme file by calling make_readme(yaml_dict)
                        if yaml_dict is not None:
                            readme = make_readme(yaml_dict=yaml_dict)
                            #save readme as readme.md
                            with open(f'{root}/readme.md', 'w') as readme_file:
                                try:
                                    readme_file.write(readme)
                                except Exception as e:
                                    print(f'error creating readme for {root} most likely no working.yaml file/n')
                                    print(e)
                                pass
                        counter += 1
                        #print a dot every 100 times through
                        if counter % 100 == 0:
                            print('.', end='', flush=True)

                    #except Exception as e:
                    #    print(f'error creating readme for {root} most likely no working.yaml file/n')
                    #    print(e)
                    #    pass
    print()

def make_readme(**kwargs):
    yaml_dict = kwargs['yaml_dict']
    #if yaml_dict is an array take element
    if type(yaml_dict) is list:
        yaml_dict = yaml_dict[0]

    yaml_table =  oom_base.yaml_to_markdown(**kwargs)
    name = yaml_dict.get('name', '')
    owner = yaml_dict.get('owner', '')
    
    ## links
    links = yaml_dict.get('links', '')
    url = ""
    github_path = ""
    if links != '':
        url = links.get('github_src_repo', '')
        github_path = links.get('github_src', '')
        
    ## footprint details
    footprint = yaml_dict.get('footprint', '')
    description = ""
    libraryLink = ""
    number_of_pads = ""
    if footprint != '':
        description = footprint.get('description', '')
        libraryLink = footprint.get('libraryLink', '')
        number_of_pads = footprint.get('number_of_pads', '')

    readme = f"""# {name} by {owner}  
This is a harvested standardized copy of a footprint from github.  
The original project can be found at:  
{url}  
The original footprint can be found at:
{github_path}
Please consult that link for additional, details, files, and license information.  
## Footprint Details
* description: {description}  
* libraryLink: {libraryLink}  
* number_of_pads: {number_of_pads}  
## yaml dump  
{yaml_table}
"""
    return readme


def make_readme_old(**kwargs):
    yaml_dict = kwargs['yaml_dict']
    yaml_dict = yaml_dict[0]
    url = yaml_dict['url']
    owner = yaml_dict['owner']['login']
    name = yaml_dict['name']
    github_path = str(yaml_dict['github_path'])
    description = ""
    if 'description' in yaml_dict:
        description = yaml_dict['description']
    libraryLink = ""
    if 'libraryLink' in yaml_dict:
        libraryLink = yaml_dict['libraryLink']
    number_of_pads = ""
    if 'number_of_pads' in yaml_dict:
        number_of_pads = yaml_dict['number_of_pads']

    oomp_key = yaml_dict.get('oomp_key', '')

    readme = f"""        
# {name} by {owner}  
This is a harvested standardized copy of a footprint from github.  
The original project can be found at:  
{url}  
The original footprint can be found at:  
{github_path}  
  
Please consult that link for additional, details, files, and license information.  
## Oomp Details
* oomp_key: {oomp_key}
## Footprint Details  
* description: {description}  
* libraryLink: {libraryLink}  
* number_of_pads: {number_of_pads}  
 
  
Note: It was auto harvested and if the original repo had more than one board file or anything out of the ordinary the files here are likely not representative.  
    """
    return readme

def get_footprint_details(**kwargs):
    
    footprint = kwargs['footprint']
    return_value = {}
    try:
        return_value['description'] = footprint.description
        try:
            return_value['libraryLink'] = footprint.libraryLink
        except:
            return_value['libraryLink'] = footprint.libId
        return_value['number_of_pads'] = len(footprint.pads)
    except Exception as e:
        print(f'error getting footprint details')
        #print(e)
        pass
    return return_value

def get_repo_details(**kwargs):
    repo_url = kwargs['repo_url']
    repo_name = repo_url.split('/')[-1]
    repo_owner = repo_url.split('/')[-2]

    #see if the repo details are already loaded
    if repo_url in github_repo_details:
        return github_repo_details[repo_url]
    else:
        #get the repo detailsffrom github api
        import requests
        #request the repo details via api
        url = f'https://api.github.com/repos/{repo_owner}/{repo_name}'
        r = requests.get(url)
        #convert to json
        repo_details = r.json()
        #add to github_repo_details
        github_repo_details[repo_url] = repo_details
        #delay 10 seconds
        import time
        time.sleep(10)
        return repo_details
        





    