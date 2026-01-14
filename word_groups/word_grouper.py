


import math
import sys


MORMON = [
    "author/mormon/book_of_mormon_intro.txt", 
    "author/mormon/mormon_book_of_mosiah.txt", 
    "author/mormon/mormon_in_4_nephi.txt", 
    "author/mormon/mormon_in_mormon.txt", 
    "author/mormon/mormon_words_of_mormon.txt", 
    "author/mormon/mormon_book_of_alma.txt", 
    "author/mormon/mormon_in_3_nephi.txt", 
    "author/mormon/mormon_in_helaman.txt",
    "author/mormon/mormon_in_moroni.txt"
]
MORMON_OUT = "word_groups/mormon_phrases"

NEPHI = [
    "author/nephi/2nd_nephi_excerpts.txt",
    "author/nephi/first_nephi_excerpts.txt"
]
NEPHI_OUT = "word_groups/nephi_phrases"

ALMA_YOUNGER = [
    "author/alma_younger/alma_younger_alma.txt",
    "author/alma_younger/alma_younger_mosiah.txt"
]
ALMA_YOUNGER_OUT = "word_groups/alma_younger_phrases"

AMMON = [
    "author/ammon/ammon_in_alma.txt"
]
AMMON_OUT = "word_groups/ammon_phrases"




MODE = "GET_PHRASES"
FILES = AMMON
OUTPUT = AMMON_OUT
min_count = 3

# MODE = "SEARCH"
SEARCH_PHRASE = "i would that"


def printf(open_file, text=""):
    print(text)
    open_file.write(f"{text}\n")


if MODE == "GET_PHRASES":

    with open(OUTPUT, 'w') as out_f:
        # collect phrase counts
        phrase_counts = {} # occurances of the phrase
        for file in FILES:

            printf(out_f, f"Processing {file}...")

            phrase_length = 6
            with open(file, 'r') as f:
                text = f.read().lower()
                words = text.split()
                while phrase_length > 0:
                    for i in range(len(words) - phrase_length + 1):
                        phrase = ' '.join(words[i:i + phrase_length])
                        if phrase in phrase_counts:
                            phrase_counts[phrase] += 1
                        else:
                            phrase_counts[phrase] = 1
                    
                    phrase_length -= 1


        # only keep phrases that occur enough determined by the length of the data
        # threshold = len(phrase_counts) * 0.0002
        threshold = min_count
        phrase_counts = {k: v for k, v in phrase_counts.items() if v > threshold}

        # combine similar phrases in groups
        grouped_phrases = {}
        single_words = []
        print("\nGrouping phrases...", end='', flush=True)
        i = 0;
        for phrase in phrase_counts:
            
            # print progress
            sys.stdout.write("\r")  # move cursor to start of the line
            sys.stdout.write(f"Grouping phrases... {100.0*i/len(phrase_counts):.1f}%")
            sys.stdout.flush()
            i += 1

            if len(phrase.split()) > 1:
                found_group = False
                for group in grouped_phrases:
                    phrase_words = set(phrase.split())
                    group_words = set(group.split())
                    shared_words = phrase_words.intersection(group_words)
                    # add to existing group if 60% of words are shared
                    similarity = len(shared_words) / min(len(phrase_words), len(group_words))
                    if similarity >= 0.7:
                        # add to existing group
                        grouped_phrases[group].append(
                            (phrase, phrase_counts[phrase])
                        )
                        found_group = True
                        break

                if not found_group and len(phrase.split()) > 1:
                    # create new group
                    grouped_phrases[phrase] = [
                        (phrase, phrase_counts[phrase])
                    ]
            else:
                single_words.append((phrase, phrase_counts[phrase]))

        sys.stdout.write("\r")  # move cursor to start of the line
        sys.stdout.write(f"Grouping phrases... {100.0*i/len(phrase_counts):.1f}%")
        sys.stdout.flush()
        print()
        print()


        # sort and print
        print("Sorting...\n");
        def value_phrase_group(phrase_group):
            main_phrase, phrase_counts = phrase_group
            total_value = 0
            for phrase, count in phrase_counts:
                weight = count * math.log(len(phrase.split())+1)
                total_value += weight
                # total_value += count
            return total_value / len(phrase_counts)


        

        sorted_phrase_groups = sorted(grouped_phrases.items(), key=value_phrase_group, reverse=True)
        for main_phrase, phrase_counts in sorted_phrase_groups[:200]:
            phrase_counts = sorted(phrase_counts, key=lambda x: x[1], reverse=True)
            printf(out_f, f"'{main_phrase}'")
            for phrase, count in phrase_counts:
                printf(out_f, f"\t-- '{phrase}': {count}")

        printf(out_f)     
        printf(out_f, "Single words:")
        sorted_single_words = sorted(single_words, key=lambda x: x[1], reverse=True)
        for word, count in sorted_single_words[:50]:
            printf(out_f, f"'{word}': {count}")


        printf(out_f, )
        printf(out_f, f'Minimum Count: {int(threshold)}')

if MODE == "SEARCH":

    occurances = 0
    for file in FILES:

        print(f"Processing {file}...")

        phrase_length = 6
        with open(file, 'r') as f:
            text = f.read().lower()
            count = text.count(SEARCH_PHRASE)
            occurances += count
            if count > 0:
                print(f'{file} -> {count}')


    print(f'TOTAL: {occurances}')


