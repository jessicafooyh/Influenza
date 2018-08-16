from Scraper import *
import multiprocessing as mp
import numpy as np


def influencer_bin_data(influencers, user, pw):
    for i in range(len(influencers)):

        print('Extracting info from ' + influencers[i].decode('utf-8') + '... using ' + user)
        scraper = Scraper(influencers[i], user, pw)
        user_data = scraper.run()
        print('\n' + 'No. of followers scraped for ' + influencers[i].decode('utf-8') + ' : ' + str(len(user_data)))
        scraper.close()

        # save data for each user
        file_name = 'data/followers_' + influencers[i].decode('utf-8') + '.pickle'
        with open(file_name, 'wb') as file:
            pickle.dump(user_data, file)

        # track done list of users
        with open('done_list.txt', 'a') as file:
            file.write(influencers[i].decode('utf-8')+'\n')


def set_creds():
    """Set instagram credentials in lists here. Use multiple for efficient scraping."""
    users = ['instagram_username']
    pws = ['instagram_password']
    return users, pws


if __name__ == '__main__':

    with open('seed_list.txt', 'rb') as f:
        influencers = f.read().splitlines()

    with open('done_list.txt', 'rb') as f:
        done = f.read().splitlines()

    influencers = [i for i in influencers if i not in done]

    users, pws = set_creds()
    n_workers = 1 # set number of cores for multi-core processing
    workers = []
    influencer_bins = np.array_split(influencers, n_workers)

    for cpu in range(n_workers):
        worker = mp.Process(name=str(cpu),
                            target=influencer_bin_data,
                            args=(influencer_bins[cpu],
                                  users[cpu-1],
                                  pws[cpu-1]))
        worker.start()
        workers.append(worker)

    for worker in workers:
        worker.join()

    quit()




