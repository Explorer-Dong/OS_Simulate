#include <bits/stdc++.h>
#include <pthread.h>
#include <ctype.h>
#include <semaphore.h>
using i64 = unsigned long long int;

std::ofstream fout("ans.out");
sem_t mutex_write;

struct buf
{
	char* filename;
	int wc_count;
};


auto get_current_time()
{
    auto now = std::chrono::system_clock::now();
    auto timestamp = std::chrono::duration_cast<std::chrono::milliseconds>(now.time_since_epoch()).count();
    return timestamp;
};

auto start_time = get_current_time();

void* count_words(void* arg)
{
	std::vector<i64> time_vec;
	buf* ptr = (buf*)arg;
	char* filename = ptr->filename;
	FILE *fp;
	int c, prevc = '\0';
	if ((fp = fopen(filename, "r")) != NULL)
	{
		while ((c = getc(fp)) != EOF)
		{
			if (!isalnum(c) && isalnum(prevc))
			{
				auto cur = get_current_time();
				time_vec.push_back(cur - start_time);
				ptr->wc_count++;
			}
			else std::this_thread::sleep_for(std::chrono::milliseconds(100));

			prevc = c;
			std::this_thread::sleep_for(std::chrono::milliseconds(1));
		}
		if (isalnum(prevc))
		{
			auto cur = get_current_time();
			time_vec.push_back(cur - start_time);
			ptr->wc_count++;
		}
		fclose(fp);
	}
	else
		perror(filename);
	
	sem_wait(&mutex_write);
	
	fout << "File$$" << filename << "$$: ";
	for (auto time :time_vec) fout << time << " ";
	fout << "\n";
	
	sem_post(&mutex_write);
	
	pthread_exit((void*)&ptr->wc_count);
	return nullptr;
}

int main(int ac, char *av[])
{
	if (ac < 3)
	{
		printf("Usage:%s file1 file2\n", av[0]);
		return 1;
	}
	sem_init(&mutex_write, 0, 1);
	
	std::vector<buf> args(1);
	for (int i = 1; i < ac; i++)
	{
		args.push_back({av[i], 0});
	}
	
	std::vector<pthread_t> t(ac);
	for (int i = 1; i < ac; i++)
	{
		if (pthread_create(&t[i], nullptr, count_words, &args[i]) != 0)
		{
			perror("pthread_create");
			return 1;
		}
	}
	
	std::vector<void*> result(ac);

	for (int i = 1; i < ac; i++)
	{
		pthread_join(t[i], &result[i]);
	}

	int total_words = 0;
	for (int i = 1; i < ac; i++)
	{
		total_words += *((int*)result[i]);
	}
	printf("Total words: %d\n", total_words);

	sem_destroy(&mutex_write);
	return 0;
}