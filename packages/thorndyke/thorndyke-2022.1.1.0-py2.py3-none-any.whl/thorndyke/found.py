from thorndyke import colors

# The found function returns found results only
# And it can be called by specifying the -f/--found flags        
def found(args,response,site_name,site_url):
    if response.status_code == 200:      
        print(f'{colors.white}[{colors.green}+{colors.white}] {site_name}: {colors.green}{site_url.format(args.username)}{colors.reset}')