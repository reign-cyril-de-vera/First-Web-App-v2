class WebBlocker:
    def __init__(self, hosts_path, redirect_path, section_start, section_end):
        self.hosts_path = hosts_path
        self.redirect_path = redirect_path
        self.section_start = section_start
        self.section_end = section_end

    def read_hosts_file(self):
        try:
            with open(self.hosts_path, "r+") as hosts_file:
                return hosts_file.readlines()
        except FileNotFoundError:
            print("Hosts file not found.")
            return []

    def write_hosts_file(self, hosts):
        with open(self.hosts_path, "w") as hosts_file:
            hosts_file.writelines(hosts)

    def block_sites(self, site_to_block):
        hosts = self.read_hosts_file()
        if self.section_start not in hosts:
            hosts.append(self.section_start)
            hosts.append(self.section_end)
        insert_idx = hosts.index(self.section_start) + 1

        # for site in sites_to_block:
        site_edit1 = f"{self.redirect_path} {site_to_block}\n"
        site_edit2 = f"{self.redirect_path} www.{site_to_block}\n"
        
        if (site_edit1 in hosts) and (site_edit2 in hosts):
            print(f"{site_to_block} is already blocked")
        else:
            print(f"Blocking {site_to_block}")
            hosts.insert(insert_idx, site_edit1)
            hosts.insert(insert_idx + 1, site_edit2)
            insert_idx += 2
        
        self.write_hosts_file(hosts)

    def get_blocked_sites(self):
        hosts = self.read_hosts_file()
        sites_blocked = []

        for idx in range(hosts.index(self.section_start) + 1, hosts.index(self.section_end)):
            if not hosts[idx].replace(self.redirect_path + " ", "").startswith("www."):
                site = f'{hosts[idx].replace(self.redirect_path + " ", "")}'.replace("\n", "")
                sites_blocked.append(site)
        
        for i, site in enumerate(sites_blocked):
            print(f'{i+1}. {site}')
        
        return sites_blocked

    def unblock_site(self, site_to_unblock):
        hosts = self.read_hosts_file()
        hosts.remove(f'{self.redirect_path} {site_to_unblock}\n')
        hosts.remove(f'{self.redirect_path} www.{site_to_unblock}\n')
        self.write_hosts_file(hosts)

if __name__ == "__main__":
    hosts_path = "C:/Windows/System32/drivers/etc/hosts"       # for implementation
    # hosts_path = "hosts"                                         # for development
    redirect_path = "127.0.0.1"
    section_start = "# Web blocker section start\n"
    section_end = "# Web blocker section end\n"
    
    web_blocker = WebBlocker(hosts_path, redirect_path, section_start, section_end)
    
    while True:
        print("\nGood day!\n1. Block Sites\n2. Unblock Sites\n3. Exit")
        action = int(input("What do you want to do? "))
        if action == 1:
            print("\nSites currently blocked:")
            web_blocker.get_blocked_sites()
            site_to_block = input("What site would you want to block? ")
            web_blocker.block_sites(site_to_block)
        elif action == 2:
            print("\nSites currently blocked:")
            blocked_sites = web_blocker.get_blocked_sites()
            if blocked_sites:
                site_to_unblock = blocked_sites[int(input("Please enter the site to unblock: ")) - 1]
                web_blocker.unblock_site(site_to_unblock)
        elif action == 3:
            print("\nHave a good day!")
            exit()
        else:
            print("\nPlease enter a valid action.")
    
    
