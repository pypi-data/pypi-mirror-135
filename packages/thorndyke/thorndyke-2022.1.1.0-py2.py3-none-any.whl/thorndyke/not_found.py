from thorndyke import colors

# The notfound function returns not found results only
# And it can be called by specifying the -n/--not-found flags
def not_found(args,response,site_name,site_url,data):
    if response.status_code != 200:
    	print(f'{colors.white}[{colors.red}-{colors.white}] {site_name}: {colors.red}Not Found{colors.reset}')