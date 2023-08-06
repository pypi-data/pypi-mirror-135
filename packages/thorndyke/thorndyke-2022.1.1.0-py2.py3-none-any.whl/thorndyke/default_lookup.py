from thorndyke import colors

# The normal function will return both found and not found results
# This is called by default if both the  -f/--found & -n/--not-found flags are not specified
def default(args,response,site_url,site_name):
    if response.status_code == 200:
    	print(f'{colors.white}[{colors.green}+{colors.white}] {site_name}: {colors.green}{site_url.format(args.username)}{colors.reset}')
    else:
    	print(f'{colors.white}[{colors.red}-{colors.white}] {site_name}: {colors.red}Not Found{colors.reset}')