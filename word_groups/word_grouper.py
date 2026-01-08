


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



FILES = MORMON


# collect phrase counts
phrase_counts = {} # occurances of the phrase
for file in FILES:

    print(f"Processing {file}...")

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
threshold = len(phrase_counts) * 0.0002
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
        total_value += count
    return total_value

sorted_phrase_groups = sorted(grouped_phrases.items(), key=value_phrase_group, reverse=True)
for main_phrase, phrase_counts in sorted_phrase_groups[:200]:
    phrase_counts = sorted(phrase_counts, key=lambda x: x[1], reverse=True)
    print(f"'{main_phrase}'")
    for phrase, count in phrase_counts:
        print(f"\t-- '{phrase}': {count}")

print()     
print("Single words:")
sorted_single_words = sorted(single_words, key=lambda x: x[1], reverse=True)
for word, count in sorted_single_words[:50]:
    print(f"'{word}': {count}")








