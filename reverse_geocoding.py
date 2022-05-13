import geocoder
import addfips

af = addfips.AddFIPS()


##Gets the county based on lat. and long. columns.
def county(x):
    g = geocoder.osm([x.lat, x.long], method='reverse').json
    if g:
        return g.get('county')
    else:
        return 'no county'

##Gets County FIPS code– important for matching to census data, eventually.
def cFIPS(x):
    cFIPS = af.get_county_fips(x.county, x.state)
    return cFIPS

##Gets State FIPS code, because I like to be safe. This step is probably redundant.
def sFIPS(x):
    sFIPS = af.get_state_fips(x)
    return sFIPS

##Puts it all together, and drops non-US and North American rows, because territories were being tricky.
def reverse_geo(df):
    df.drop(df.index[df['country'] != 'United States of America'], axis=0, inplace=True)
    df.drop(df.index[df['continent'] != 'North America'], axis=0, inplace=True)
    df['county'] = df[['lat', 'long']].apply(lambda x: county(x), axis=1)
    df['countyFIPS'] = df[['county', 'state']].apply(lambda x: cFIPS(x), axis=1)
    df['stateFIPS'] = df['state'].apply(lambda x: sFIPS(x))
    return df

