import os
import yaml

def find_docker_compose_files(directory):
    files = []
    for root, dirs, filenames in os.walk(directory):
        for filename in filenames:
            if filename in ['docker-compose.yml', 'compose.yml', 'compose.yaml', 'docker-compose.yaml']:
                files.append(os.path.join(root, filename))
    return files

def check_ports_used(compose_file_paths):
    used_ports = set()
    errors = []
    
    for path in compose_file_paths:
        with open(path, 'r') as file:
            try:
                data = yaml.safe_load(file)
            except yaml.YAMLError as exc:
                print(f"An error occured while processing YAML file {path}: {exc}")
                continue
            
            services = data.get('services', {})
            for service_name, service_config in services.items():
                ports = service_config.get('ports', [])
                for port_mapping in ports:
                    host_port = port_mapping.split(':')[0]
                    if int(host_port) < 5000 or int(host_port) > 5999:
                        errors.append(f"Port {host_port} must be between 5000 and 5999 in file {path}.")
                    if host_port in used_ports:
                        errors.append(f"Port {host_port} already using in file {path}.")
                    else:
                        used_ports.add(host_port)
    
    if errors:
        for error in errors:
            print(error)
        raise Exception("There are duplicating ports in docker-compose files.")
    else:
        print("All public ports are unique.")

if __name__ == "__main__":
    directory = 'tasks'
    compose_files = find_docker_compose_files(directory)
    check_ports_used(compose_files)
