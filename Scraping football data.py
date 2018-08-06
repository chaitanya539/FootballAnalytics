#importing libraries
from selenium import webdriver
import re
import pandas as pd
import numpy as np
import time


log = []
no_summary_data_players = []
probable_incorrect_selection = pd.DataFrame()

#declaring master dataframes 
Fact_summary = pd.DataFrame()
Fact_shots = pd.DataFrame()
Fact_goals = pd.DataFrame()
Fact_dribbles = pd.DataFrame()
Fact_possession_loss = pd.DataFrame()
Fact_aerial = pd.DataFrame()
Fact_tackles = pd.DataFrame()
Fact_interception = pd.DataFrame()
Fact_fouls = pd.DataFrame()
Fact_cards = pd.DataFrame()
Fact_offsides = pd.DataFrame()
Fact_clearances = pd.DataFrame()
Fact_blocks = pd.DataFrame()
Fact_saves = pd.DataFrame()
Fact_passes = pd.DataFrame()
Fact_key_passes = pd.DataFrame()
Fact_assists = pd.DataFrame()

#reading data from Dim_Player

#dim_player = pd.read_excel('Dim_Players.xlsx')
#dim_player = pd.read_excel('portugal vs spain.xlsx')
dim_player = pd.read_excel('dim_repaining_players.xlsx')

#Situational
#dim_player = dim_player[~dim_player.Player.isin(pd.unique(Fact_summary.Player).tolist())]

#reprocess_log.columns = ['Player']
player = dim_player.iloc[:,2]
player = list(player)
player_club = dim_player['Club']
player_club = list(player_club)


def chrome_master(restart):
    try:
        if(restart == 1):
            global mydriver
            mydriver.quit()
            baseurl = "https://www.whoscored.com/Search/?t="
            mydriver = webdriver.Chrome(executable_path=r"chromedriver.exe")
            mydriver.get(baseurl)
            mydriver.maximize_window()
        if(restart == 0):
            baseurl = "https://www.whoscored.com/Search/?t="
            mydriver = webdriver.Chrome(executable_path=r"chromedriver.exe")
            mydriver.get(baseurl)
            mydriver.maximize_window()
        return mydriver
    except:
        print("Error: Chrome wasn't initialized")
        

def search_player(mydriver, player_index):
    try:
        mydriver.find_element_by_id('search-box').send_keys(player[player_index])
        mydriver.find_element_by_id('search-button').click()
        print('\n','\n',"searching whoscore for " + player[player_index])
        
        #do i need a try except block?
    except:
        print("What the hell? why didn't the search bar didn't load? try triggering chrome master inside this except bloc" )
              
    
# table scrapper function
def table_scraper(table_name, element, head = 0, body = 0):
    row_elements = []
    table_name = pd.DataFrame()
    if(head == 1):
        for i in element.find_elements_by_xpath('.//tr'):
            for j in i.find_elements_by_xpath('.//th'):
                row_elements.append(j.text)
                #print(row_elements)
            q = pd.DataFrame(np.array(row_elements).reshape(1,len(row_elements)))
            table_name=table_name.append(q)
            row_elements = []
    if(body == 1):
        for i in element.find_elements_by_xpath('.//tr'):
            for j in i.find_elements_by_xpath('.//td'):
                row_elements.append(j.text)
                #print(row_elements)
            q = pd.DataFrame(np.array(row_elements).reshape(1,len(row_elements)))
            table_name=table_name.append(q)
            row_elements = []
    if(head!= 1 and body != 1 ):
        print("need to pass atleast one of 'head' or 'body' of the table")
    return table_name



def reffer_google():
    global player_index, player,mydriver
    baseurl1 = "https://www.google.com"
    mydriver = webdriver.Chrome(executable_path=r"chromedriver.exe")
    mydriver.get(baseurl1)    
    mydriver.find_element_by_id("lst-ib").send_keys(player[player_index] + " whoscored.com \n")
    #mydriver.find_element_by_xpath("//*[@id='tsf']/div[2]/div[3]/center/input[1]").click()
    mydriver.find_element_by_xpath("//*[@id='rso']/div/div/div[1]/div/div/h3/a").click()
    try:
        mydriver.find_element_by_xpath("//div[@id='sub-navigation']/ul/li[1]/a")
    except:
        mydriver.quit()
    return mydriver

#generic to be function for clicking right button
 
def click_correct_search_result(player_index, sleep_seconds):
    global mydriver, search_table, player, player_club,probable_incorrect_selection
    var = 0
    search_index = 0
    #if length of search table is 2 then directly click the link other wise compare to the club
    if(len(search_table)==1):
        print("no data found for player " + player[player_index])
    
    if(len(search_table) == 2):
        while(var==0):
            time.sleep(sleep_seconds)    
            try:
                mydriver.find_elements_by_xpath('//a[@class="iconize iconize-icon-left"]')[0].click()
                var = 1
            except:
                var = 0
    
    if(len(search_table) > 2):
        #getting the correct element of the table to be clicked on i.e. index
        #remove header column from the search table
        #remove the age column        
        search_table = search_table.iloc[1:,0:2]
        #replacing all the blanks by nans
        search_table = search_table.replace(r'', np.nan, regex=True)
        search_table = search_table.replace(r'^\s+$', np.nan, regex=True)
        try:
            y = 0     
            search_array = []  
            for y in range(0, len(search_table)):
               search_array.extend(search_table.iloc[y].tolist())
            search_array = [item for item in search_array if str(item) != 'nan' ]
            search_index = search_array.index(player_club[player_index]) - 1
        except ValueError:
            search_index = 0
            print('Player club value does not match the dim player value or club/team not mentioned in search result')
            probable_incorrect_selection = probable_incorrect_selection.append(pd.DataFrame(np.array([player[player_index],player_club[player_index]]).reshape(1,2)))
        while(var == 0):
            time.sleep(sleep_seconds)
            try:
                mydriver.find_elements_by_xpath('//a[@class="iconize iconize-icon-left"]')[search_index].click()
                var = 1
            except:
                var = 0
    if(len(search_table)==0):
        try:
            mydriver.find_elements_by_xpath('//a[@class="iconize iconize-icon-left"]')[0].click()
        except:
            print("log: search indexing failed for " + player[player_index])
    return search_table, search_index

def tab_selection(sleep_seconds):
    global mydriver
    var = 0
    mydriver.implicitly_wait(1)
    try:
        mydriver.find_element_by_xpath("//div[@id='sub-navigation']/ul/li[4]/a").click()
        history_tab = 1
    except:
        print('History tab not found')
        history_tab = 0
    
    if(history_tab == 1):
        #clicking the details button for a player
        while(var==0):
            time.sleep(sleep_seconds)
            try:
                mydriver.find_elements_by_xpath('//div[@id="player-tournament-stats"]/ul[@id="player-tournament-stats-options"]/li[5]/a')[0].click()
                #for select accumulation criterion as "total"
                mydriver.find_element_by_xpath("//select[@id='statsAccumulationType']/option[@value='2']").click()
                
                mydriver.find_element_by_xpath("//select[@id='category']/optgroup[@label='Offensive']/option[@value='aerial']").click()
                #mydriver.find_element_by_xpath("//select[@id='statsAccumulationType']/option[@value='4']").click()
                #time.sleep(1)
                
                #mydriver.find_element_by_xpath("//select[@id='statsAccumulationType']/option[@value='2']").click()
                #For selecting tackle in category option within defensive option group
                var = 1
                print("the tabs were correctly selected")
            except:
                var = 0
                print("the tabs weren't correctly selected")
            
    if(history_tab ==0):
        print("history tab not found, scraping data for summary tab")
    
    return history_tab


def table_data(sleep_seconds):
    global mydriver
    var = 0
    c = 0
    while(var==0):
        time.sleep(sleep_seconds)
        c=0
        head_title = mydriver.find_elements_by_xpath("//table[@id='top-player-stats-summary-grid']/thead")
        for l in head_title:
            c=c+1
            #print (l.text)
            var = len(l.text)
            if var>0:
                data_headers=head_title
                
    var1 = 0
    c1 = 0
    while(var1==0):
        time.sleep(sleep_seconds)
        c1=0
        table = mydriver.find_elements_by_xpath("//table[@id='top-player-stats-summary-grid']/tbody")
        for ii in head_title:
            c1=c1+1
            #print (ii.text)
            var1 = len(ii.text)
            if var1>0:
                data_body=table
    return data_headers, data_body, c, c1

#correcting tournament names and replacing it by its correct version
def get_tournament_name():
    global search_table, element_body, a1
    if(len(search_table)!=1):
        Tournament = []
        for q in element_body[a1-1].find_elements_by_xpath('.//tr'):
            raw_html = q.get_attribute('innerHTML')
            match = re.search('Tournaments/(.*)<span',raw_html)
            try:
                Tournament.append(match.group(1))
            except:
                print("No further matches found for tournament name!")
        
        for i in range(0,len(Tournament)):
            match = re.search('/(.*)"',Tournament[i]) #---> induce i here
            #Removing first and last characters of the string - cleaning
            temp = list(match[0])
            temp.pop(0)
            temp.pop(-1)
            temp = ''.join(temp)
            Tournament[i] = temp
    if(len(Tournament)!=0):
        print(str(len(Tournament)) + ' Matches found for full tournament names!' )
    else:
        print("tournament list was empty, thus there might be no data fot this player")
    return Tournament
    

def remove_player(a):       
    global Fact_aerial,Fact_shots,Fact_goals,Fact_dribbles,Fact_possession_loss,Fact_tackles, Fact_interception, Fact_fouls,Fact_cards, Fact_offsides, Fact_clearances, Fact_blocks, Fact_saves, Fact_passes, Fact_key_passes, Fact_assists
    Fact_aerial = Fact_aerial[~Fact_aerial.Player.isin(a)]
    Fact_shots = Fact_shots[~Fact_shots.Player.isin(a)]
    Fact_goals = Fact_goals[~Fact_goals.Player.isin(a)]
    Fact_dribbles = Fact_dribbles[~Fact_dribbles.Player.isin(a)]
    Fact_possession_loss = Fact_possession_loss[~Fact_possession_loss.Player.isin(a)]
    Fact_tackles = Fact_tackles[~Fact_tackles.Player.isin(a)]
    Fact_interception = Fact_interception[~Fact_interception.Player.isin(a)]
    Fact_fouls = Fact_fouls[~Fact_fouls.Player.isin(a)]
    Fact_cards = Fact_cards[~Fact_cards.Player.isin(a)]
    Fact_offsides = Fact_offsides[~Fact_offsides.Player.isin(a)]
    Fact_clearances = Fact_clearances[~Fact_clearances.Player.isin(a)]
    Fact_blocks = Fact_blocks[~Fact_blocks.Player.isin(a)]
    Fact_saves = Fact_saves[~Fact_saves.Player.isin(a)]
    Fact_passes = Fact_passes[~Fact_passes.Player.isin(a)]
    Fact_key_passes = Fact_key_passes[~Fact_key_passes.Player.isin(a)]
    Fact_assists = Fact_assists[~Fact_assists.Player.isin(a)]
    
def data_check(df_body):
    dfs = [Fact_aerial[Fact_aerial.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_shots[Fact_shots.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_goals[Fact_goals.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_dribbles[Fact_dribbles.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_possession_loss[Fact_possession_loss.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_tackles[Fact_tackles.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_interception[Fact_interception.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_fouls[Fact_fouls.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_cards[Fact_cards.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_offsides[Fact_offsides.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_clearances[Fact_clearances.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_blocks[Fact_blocks.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_saves[Fact_saves.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_passes[Fact_passes.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_key_passes[Fact_key_passes.Player.isin(pd.unique(df_body.Player).tolist())],
    Fact_assists[Fact_assists.Player.isin(pd.unique(df_body.Player).tolist())]]

    f = pd.DataFrame()
    for i in range(0,len(dfs)):
        grouped = dfs[i].groupby(dfs[i].Player)
        f1 = pd.DataFrame(grouped['Player'].agg(np.count_nonzero))
        f1.columns = [i]
        f = pd.concat([f, f1], axis=1)
        
    d = f.transpose()
    a = []
    for column in d:
        if(d[column].mean() != d[column].median()):
            a.append(column)
            print("removing the data for player - " + column +"..." )
            remove_player(a)
        else:
            print("data is correct for the player - "+column)    
    return a

def data_check_full():
    global dfs
    f = pd.DataFrame()
    for i in range(0,len(dfs)):
        grouped = dfs[i].groupby(dfs[i].Player)
        f1 = pd.DataFrame(grouped['Player'].agg(np.count_nonzero))
        f1.columns = [i]
        f = pd.concat([f, f1], axis=1)
        
    d = f.transpose()
    a = []
    for column in d:
        if(d[column].mean() != d[column].median()):
            a.append(column)
            print("removing the data for player - " + column +"..." )
            remove_player(['Christian Eriksen'])
        else:
            print("data is correct for the player - "+column)    
    return a

whoscore_dict = {'Offensive': ['aerial','shots','goals','dribbles','possession-loss'],
                 'Defensive': ['tackles','interception','fouls','cards','offsides','clearances','blocks','saves'],
                 'Passing':['passes','key-passes','assists']}
#whoscore_dict = {'Offensive': ['aerial','shots','goals']}


player_index = 0
#opening up the chrome and navigating to whoscore.com
''' Pass 0 for first time initializing, 1 for restarting of chrome'''
mydriver = chrome_master(0)



while(player_index < len(player)):
    # In case of multiple results, search for the correct row to click
    print("search for player index number: " + str(player_index))
    don = 0
    cnt = 0
    while(don==0):
        try:
            search_player(mydriver, player_index)
            try:
                player_search_results =  mydriver.find_elements_by_xpath("//div[@class='search-result']/table/tbody")[0]
            except:
                mydriver.find_element_by_xpath("//span[@class='search-suggestion']/a").click()
                player_search_results =  mydriver.find_elements_by_xpath("//div[@class='search-result']/table/tbody")[0]
                
            search_table = pd.DataFrame()
            search_table = table_scraper(search_table,player_search_results,0,1)
            search_table , search_index = click_correct_search_result(player_index,1) #enter player_index, sleep time
            don = 1
        except:
             mydriver.quit()
             try:
                 mydriver = reffer_google()
                 don = 1
             except:
                 print("google search wasn't right :( ")
                 log.append(player[player_index])
                 try:
                     mydriver.quit()
                 except:
                     pass
                 mydriver = chrome_master(0)
                 player_index = player_index +1
                 don = 0
             
        #try to select history tab 
    try:
        history_tab = tab_selection(2)
        mydriver.find_element_by_xpath("//div[@id='sub-navigation']/ul/li[1]/a")
    except:
        history_tab = -1
        try:
            mydriver.quit()
        except:
            pass
        mydriver = chrome_master(0)            
        
    
    
    
    if(history_tab != 0):
        for key, values in whoscore_dict.items() :
            for value in values:
                vlaue_aquired = 0
                times_tried = 0
                while(vlaue_aquired ==0):
                    time.sleep(1)
                    try:
                        print("fetching values for " + key , value)
                        mydriver.find_element_by_xpath("//select[@id='category']/optgroup[@label='"+key+"']/option[@value='"+value+"']").click()
                        element_head, element_body, a, a1 = table_data(2)
                        df_head = pd.DataFrame()
                        df_head = table_scraper(df_head,element_head[a-1],1,0)
                        df_body = pd.DataFrame()
                        df_body = table_scraper(df_head,element_body[a1-1],0,1)
                        #making headers
                        df_body.columns = df_head.iloc[0,:]
                        #removing last row of totals
                        df_body = df_body[:-1]
                        #inserting player name
                        df_body.insert(0,'Player', player[player_index])
                        #get tournament full names
                        Tournament = get_tournament_name()
                        print("records found for " + player[player_index] +" for "+ str(key)+ " " + str(value) + " are: " + str(len(df_body)))
                        if(len(df_body)>=1):
                            #Replacing tournament names with full names
                            df_body.insert(df_body.columns.get_loc('Tournament'), 'Tournament-fullname', Tournament)
                            
                        if(value == 'shots'):
                             df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total', 'OutOfBox', 'SixYardBox', 'PenaltyArea', 'Rating']]
                             df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total_Shots', 'OutOfBox', 'SixYardBox', 'PenaltyArea', 'Rating']
                             Fact_shots = Fact_shots.append(df_body)
                             vlaue_aquired = 1
                        if(value == 'goals'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total', 'SixYardBox', 'PenaltyArea', 'OutOfBox', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total_Goals', 'SixYardBox_Goals', 'PenaltyArea_Goals', 'OutOfBox_Goals', 'Rating']
                            Fact_goals = Fact_goals.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'dribbles'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Unsuccessful', 'Successful', 'Total Dribbles', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Unsuccessful', 'Successful', 'Total_Dribbles', 'Rating']
                            Fact_dribbles = Fact_dribbles.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'possession-loss'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'UnsuccessfulTouches', 'Dispossessed', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'UnsuccessfulTouches', 'Dispossessed', 'Rating']
                            Fact_possession_loss = Fact_possession_loss.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'aerial'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total', 'Won', 'Lost', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total_Aerial_Duels', 'Won', 'Lost', 'Rating']
                            Fact_aerial = Fact_aerial.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'tackles'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'TotalTackles', 'DribbledPast', 'TotalAttemptedTackles',
                               'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'TotalTackles', 'DribbledPast', 'TotalAttemptedTackles',
                               'Rating']
                            Fact_tackles = Fact_tackles.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'interception'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total_Interceptions', 'Rating']
                            Fact_interception = Fact_interception.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'fouls'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Fouled', 'Fouls', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Fouled', 'Fouls', 'Rating']
                            Fact_fouls = Fact_fouls.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'cards'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Yellow', 'Red', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Yellow', 'Red', 'Rating']
                            Fact_cards = Fact_cards.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'offsides'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'CaughtOffside', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'CaughtOffside', 'Rating']
                            Fact_offsides = Fact_offsides.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'clearances'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total_Clearances', 'Rating']
                            Fact_clearances = Fact_clearances.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'blocks'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'ShotsBlocked', 'CrossesBlocked', 'PassesBlocked', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'ShotsBlocked', 'CrossesBlocked', 'PassesBlocked', 'Rating']
                            Fact_blocks = Fact_blocks.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'saves'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total', 'SixYardBox', 'PenaltyArea', 'OutOfBox', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total_Saves', 'Saves_In_SixYardBox', 'Saves_In_PenaltyArea', 'Saves_From_OutOfBox', 'Rating']
                            Fact_saves = Fact_saves.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'passes'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total', 'AccLB', 'InAccLB', 'AccSP', 'InAccSP', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total_Passes', 'AccLB', 'InAccLB', 'AccSP', 'InAccSP', 'Rating']
                            Fact_passes = Fact_passes.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'key-passes'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total', 'Long', 'Short', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Total_Key_Passes', 'Long', 'Short', 'Rating']
                            Fact_key_passes = Fact_key_passes.append(df_body)
                            vlaue_aquired = 1
                        if(value == 'assists'):
                            df_body = df_body[['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Cross', 'Corner', 'Throughball', 'Freekick', 'Throwin',
                               'Other', 'Total', 'Rating']]
                            df_body.columns = ['Player', 'Season', 'Team', 'Tournament-fullname', 'Tournament', 'Apps',
                               'Mins', 'Cross', 'Corner', 'Throughball', 'Freekick', 'Throwin',
                               'Other', 'Total_Assists', 'Rating']
                            Fact_assists = Fact_assists.append(df_body)
                            vlaue_aquired = 1
                    except:
                        log.append(player[player_index])
                        pass
                    times_tried = times_tried + 1
                    if(times_tried >=4):
                        mydriver.refresh()
                        tab_selection(2)
                    if(history_tab == -1):
                        break
    #player_index = player_index +1
    #storing the data in proper dataframe
 
    try:
        if(history_tab == 0):
            time.sleep(1)
            element_head, element_body, a, a1 = table_data(2)
            df_head = pd.DataFrame()
            df_head = table_scraper(df_head,element_head[a-1],1,0)
            df_body = pd.DataFrame()
            df_body = table_scraper(df_head,element_body[a1-1],0,1)
            #making headers
            df_body.columns = df_head.iloc[0,:]
            #removing last row of totals
            df_body = df_body[:-1]
            #inserting player name
            df_body.insert(0,'Player', player[player_index])
            #get tournament full names
            Tournament = get_tournament_name()
            if(len(df_body)!=1):
                #Replacing tournament names with full names
                df_body.insert(df_body.columns.get_loc('Tournament'), 'Tournament-fullname', Tournament)
                Fact_summary = Fact_summary.append(df_body)
            if(len(df_body)==1):
                no_summary_data_players.append(player[player_index])
                print("no summary data from " + player[player_index] )
                
    except:
        log.append(player[player_index])
        #player_index = player_index +1

    player_index = player_index+1
    
     
    if(player_index%10==1 or player_index == len(player)):       
        Fact_shots.to_csv('Fact_shots.csv')
        Fact_goals.to_csv('Fact_goals.csv')
        Fact_dribbles.to_csv('Fact_dribbles.csv')
        Fact_possession_loss.to_csv('Fact_possession_loss.csv')
        Fact_aerial.to_csv('Fact_aerial.csv')
        Fact_tackles.to_csv('Fact_tackles.csv')
        Fact_interception.to_csv('Fact_interception.csv')
        Fact_fouls.to_csv('Fact_fouls.csv')
        Fact_cards.to_csv('Fact_cards.csv')
        Fact_offsides.to_csv('Fact_offsides.csv')
        Fact_clearances.to_csv('Fact_clearances.csv')
        Fact_blocks.to_csv('Fact_blocks.csv')
        Fact_saves.to_csv('Fact_saves.csv')
        Fact_passes.to_csv('Fact_passes.csv')
        Fact_key_passes.to_csv('Fact_key_passes.csv')
        Fact_assists.to_csv('Fact_assists.csv')
        Fact_summary.to_csv('Fact_summary.csv')
        
        
    if(player_index%10==1 or player_index == len(player)):
        ab = pd.DataFrame()
        ab.append(log)
        ab.to_csv('error_log_players.csv')



'''end of data scraping. now reprocessing on a case by case basis'''


dfs = [Fact_aerial,
Fact_shots,
Fact_goals,
Fact_dribbles,
Fact_possession_loss,
Fact_tackles,
Fact_interception,
Fact_fouls,
Fact_cards,
Fact_offsides,
Fact_clearances,
Fact_blocks,
Fact_saves,
Fact_passes,
Fact_key_passes,
Fact_assists]

reprocess = data_check_full()
dim_player = dim_player[dim_player.Player.isin(reprocess)]
#reprocess_log.columns = ['Player']
player = dim_player.iloc[:,2]
player = list(player)
player_club = dim_player['Club']
player_club = list(player_club)

'''
Function that takes in a df , classifies it into a shots or goals or tackles (and likewise),
checks the length of that df before and after appending into the respective fact_skill table
Then check the key column of every df otherwise reprocess--> can be put just after data scraping
for a particular ket-value pair
and finally put checks on the merged table
'''

Fact_goals.columns        
Fact_shots.columns       
        
s1 = pd.merge(Fact_shots, Fact_goals, how='inner', left_on=['Unnamed: 0', 'Player', 'Season', 'Team', 'Tournament-fullname',
       'Tournament', 'Apps', 'Mins', 'Total_Shots', 'OutOfBox', 'SixYardBox',
       'PenaltyArea', 'Rating'], right_on = ['Unnamed: 0', 'Player', 'Season', 'Team', 'Tournament-fullname',
       'Tournament', 'Apps', 'Mins', 'Total_Goals', 'SixYardBox',
       'PenaltyArea', 'OutOfBox', 'Rating'])
        
del Fact_goals['Unnamed: 0']

for key, values in whoscore_dict.items() :
    for value in values:
        print("del Fact_"+value+"['Unnamed: 0']") 
    
del Fact_shots['Unnamed: 0']
del Fact_goals['Unnamed: 0']
del Fact_dribbles['Unnamed: 0']
del Fact_possession_loss['Unnamed: 0']
del Fact_aerial['Unnamed: 0']
del Fact_tackles['Unnamed: 0']
del Fact_interception['Unnamed: 0']
del Fact_fouls['Unnamed: 0']
del Fact_cards['Unnamed: 0']
del Fact_offsides['Unnamed: 0']
del Fact_clearances['Unnamed: 0']
del Fact_blocks['Unnamed: 0']
del Fact_saves['Unnamed: 0']
del Fact_passes['Unnamed: 0']
del Fact_key_passes['Unnamed: 0']
del Fact_assists['Unnamed: 0']        
        
        

'''Code to find players with no data on whoscore'''
from selenium.common.exceptions import NoSuchElementException


player_index = 208 #Adem Ljajić

Fact_aerial = pd.read_csv('Fact_aerial.csv')
Fact_summary = pd.read_csv('Fact_summary.csv')
players_with_data = pd.unique(Fact_aerial.Player).tolist()
players_with_data.extend(pd.unique(Fact_summary.Player).tolist())

dim_player = dim_player[~dim_player.Player.isin(players_with_data)]

chrome_master(0)
reprocess_log = []
player_without_data = []
player_index = 0

while(player_index < len(player)):
    time.sleep(2)
    search_player(mydriver, player_index)
    try:
        d = mydriver.find_element_by_xpath("//*[@id='layout-content-wrapper']/div[2]/span")
        print(player[player_index] + " checking if the search suggestions (if any) works...")
        try:
            mydriver.find_element_by_xpath("//span[@class='search-suggestion']/a").click()
        except:
            print(player[player_index] + " has no search suggestions")
        d = mydriver.find_element_by_xpath("//*[@id='layout-content-wrapper']/div[2]/span")
        if( d.text[0:19] == 'No result found for'):
            print("No data found for " + player[player_index])
            player_without_data.append(player[player_index]) 
            print("this player is added to player_without_data list" )
            player_index = player_index + 1
            
    except NoSuchElementException :
        print(player[player_index] + " has data... Logging this player in reprocess_log list")
        reprocess_log.append(player[player_index])
        player_index = player_index +1
        
pd.DataFrame(reprocess_log).to_csv('reprocess_players.csv')
pd.DataFrame(player_without_data).to_csv('player_without_data.csv')

#################################################################################
#######reading files and combining###############################################



for key, values in whoscore_dict.items() :
    for value in values:
        print("Fact_"+value+" = Fact_"+value+".append(Fact_"+value+"1) ") 





for key, values in whoscore_dict.items() :
    for value in values:
        print("Fact_"+value+".drop_duplicates(keep=False, inplace=True)") 
        
Fact_shots.drop_duplicates(keep=False, inplace=True)
Fact_goals.drop_duplicates(keep=False, inplace=True)
Fact_dribbles.drop_duplicates(keep=False, inplace=True)
Fact_possession_loss.drop_duplicates(keep=False, inplace=True)
Fact_aerial.drop_duplicates(keep=False, inplace=True)
Fact_tackles.drop_duplicates(keep=False, inplace=True)
Fact_interception.drop_duplicates(keep=False, inplace=True)
Fact_fouls.drop_duplicates(keep=False, inplace=True)
Fact_cards.drop_duplicates(keep=False, inplace=True)
Fact_offsides.drop_duplicates(keep=False, inplace=True)
Fact_clearances.drop_duplicates(keep=False, inplace=True)
Fact_blocks.drop_duplicates(keep=False, inplace=True)
Fact_saves.drop_duplicates(keep=False, inplace=True)
Fact_passes.drop_duplicates(keep=False, inplace=True)
Fact_key_passes.drop_duplicates(keep=False, inplace=True)
Fact_assists.drop_duplicates(keep=False, inplace=True) 
Fact_summary.drop_duplicates(keep = False, inplace = True)       
        
        
        


Fact_shots.to_csv('Fact_shots.csv')
Fact_goals.to_csv('Fact_goals.csv')
Fact_dribbles.to_csv('Fact_dribbles.csv')
Fact_possession_loss.to_csv('Fact_possession_loss.csv')
Fact_aerial.to_csv('Fact_aerial.csv')
Fact_tackles.to_csv('Fact_tackles.csv')
Fact_interception.to_csv('Fact_interception.csv')
Fact_fouls.to_csv('Fact_fouls.csv')
Fact_cards.to_csv('Fact_cards.csv')
Fact_offsides.to_csv('Fact_offsides.csv')
Fact_clearances.to_csv('Fact_clearances.csv')
Fact_blocks.to_csv('Fact_blocks.csv')
Fact_saves.to_csv('Fact_saves.csv')
Fact_passes.to_csv('Fact_passes.csv')
Fact_key_passes.to_csv('Fact_key_passes.csv')
Fact_assists.to_csv('Fact_assists.csv')
Fact_summary.to_csv('Fact_summary.csv')





for key, values in whoscore_dict.items() :
    for value in values:
        print("print(len(pd.unique(Fact_"+value+".Player)))") 




print(len(pd.unique(Fact_shots.Player)))
print(len(pd.unique(Fact_goals.Player)))
print(len(pd.unique(Fact_dribbles.Player)))
print(len(pd.unique(Fact_possession_loss.Player)))
print(len(pd.unique(Fact_aerial.Player)))
print(len(pd.unique(Fact_tackles.Player)))
print(len(pd.unique(Fact_interception.Player)))
print(len(pd.unique(Fact_fouls.Player)))
print(len(pd.unique(Fact_cards.Player)))
print(len(pd.unique(Fact_offsides.Player)))
print(len(pd.unique(Fact_clearances.Player)))
print(len(pd.unique(Fact_blocks.Player)))
print(len(pd.unique(Fact_saves.Player)))
print(len(pd.unique(Fact_passes.Player)))
print(len(pd.unique(Fact_key_passes.Player)))
print(len(pd.unique(Fact_assists.Player)))
print(len(pd.unique(Fact_summary.Player)))

#Mohamed Salah ,'Thiago Alcantara', 'André Silva', 'Cedric Soares', 'João Mário' , 'Fedor Smolov'
#'Mansour Al-Harbi', 'Hussain Al-Mogahwi'


(pd.DataFrame(player_without_data)).to_csv('player_check.csv')

