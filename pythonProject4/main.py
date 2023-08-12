import numpy as np, matplotlib.pyplot as plt

cities = [0, 1, 2, 3, 4]  # o πολεις με νουμερα για ευκολη μεταθεση
routes = np.asarray(
    [
        [0, 4, 4, 7, 3],
        [4, 0, 2, 3, 5],
        [4, 2, 0, 2, 3],
        [7, 3, 2, 0, 6],
        [4, 5, 3, 6, 0],
    ]
)


class Population:
    def __init__(self, all_pop, routes):
        self.all_pop = all_pop  # ολος ο πληθυσμος
        self.parents = []  # στον αρχικο πληθυσμο δεν εχει προγονους
        self.score = 0  # τρεχον σκορ
        self.current_best = None  # καμια καλυτερη λυση
        self.routes = routes  # πινακας κοστους
        self.some_pop = []


def first_population(cities, routes, n):
    return Population(  # επιστρεφει n λυσεις ως τον αρχικο πληθυσμο
        np.asarray([np.random.permutation(cities[1:5]) for _ in range(n)]),
        # με τυχαιο τροπο μπλεκουμε τις πολεις, χωρις την Α που θελω να ειναι η αρχη και το τελος
        routes  # για τον αρχικο μας πληθυσμο
    )


def route_costs(self, chromosome):  # ελεγχω τον πινακα με τα κοστη και τις θεσεις των χρωμοσωματων
    add = self.routes[0, chromosome[0]] + self.routes[0, chromosome[3]] + sum(
        # για να υπολογισω την συναρτηση κοστους με συνυπολογισμο την πρωτη πολη,που δεν την μεταθετω
        [
            # προσθετω την πρωτη και την τελευταια διαδρομη για την πολη Α
            self.routes[chromosome[i], chromosome[i + 1]]
            # υπολογιζω το κοστος μεταξυ των πολεων μεσα στην μεταβλητη χρωμοσωμα
            # πχ την πολη 2 με 3 ποιο ειναι το κοστος τους
            for i in range(len(chromosome) - 1)  # μεχρι την τελευταια πολη που την υπολογισα πριν
        ]  # δεν λαμβανω υποψη το τελευταιο,και το πρωτο δεν ελεχγεται απο τον βροχο
    )  # επιστρεφει το κοστος του καθε χρωμοσωματος
    return add


Population.route_costs = route_costs


def choose_parents(self):  # μετραω για καθε λυση
    if len(self.all_pop) > 10:  # για να μενει σταθερος ο πληθυσμος,για να μεινει
        del (self.all_pop[0:len(self.bag) - 10])  # το ποσοστο του πληθυσμου που περασε στην επομενη γενια και οι γονεις
    if len(self.some_pop) > 5:  # για να μενει σταθερος ο πληθυσμος,για να μην
        del (self.some_pop[0:len(self.some_pop) - 5])  # συμμετεχουν 5 λυσεις στην διαδικασια της αναπαραγωγης
    distances = np.asarray(  # το κοστος του καθε χρωμοσωματος του πληθυσμου μου
        [self.route_costs(chromosome) for chromosome in self.all_pop[0:10]]  # και τα βαζω στην μεταβλητη που ειναι λιστα
    )  # η οποια εμπεριεχει τα κοστη του πληθισμου
    for _ in range(5):  # θα μπουν 10 τυχαιοι υποψηφιοι και 5 απο αυτους θα γίνουν γονεις
        y = np.random.uniform(0,
                              1 / distances[4] + 1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[
                                  1]+1/distances[5]+1/distances[6]+1/distances[7]+1/distances[8]+1/distances[9])  # ρουλετα
        if 1 / distances[
            0] >= y > 0:  # προς γιατι θελω το μικροτερο κοστος να εχει την μεγαλυτερη πιθ να μπει στους γονεις
            self.score = distances[0]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1 / distances[0] + 1 / distances[1] >= y > 1 / distances[0]:
            self.score = distances[1]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1 / distances[2] + 1 / distances[0] + 1 / distances[1] >= y > 1 / distances[0] + 1 / distances[1]:
            self.score = distances[2]  # διαλεγω καποιο κοστος, για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[1] >= y > 1 / distances[2] + 1 / \
                distances[0] + 1 / distances[1]:
            self.score = distances[3]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1 / distances[4] + 1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[1] >= y > 1 / \
                distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[1]:
            self.score = distances[4]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1 / distances[5] + 1 / distances[4] + 1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / \
                distances[1] >= y > 1 / distances[4] + \
                1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[1]:
            self.score = distances[4]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1/distances[6] + 1 / distances[5] + 1 / distances[4] + 1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / \
                distances[1] >= y > 1/distances[5] + 1 / distances[4] + \
                1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[1]:
            self.score = distances[4]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1/distances[7] + 1/distances[6] + 1 / distances[5] + 1 / distances[4] + 1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / \
                distances[1] >= y > 1/distances[6]+1/distances[5] + 1 / distances[4] + \
                1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[1]:
            self.score = distances[4]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1/distances[8] + 1/distances[7] + 1/distances[6] + 1 / distances[5] + 1 / distances[4] + 1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / \
                distances[1] >= y > 1/distances[7] + 1/distances[6] + 1/distances[5] + 1 / distances[4] + \
                1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[1]:
            self.score = distances[4]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
        elif 1/distances[9]+1/distances[8]+1/distances[7] + 1/distances[6] + 1 / distances[5] + 1 / distances[4] + 1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / \
                distances[1] >= y > 1/distances[8] + 1/distances[7]+ 1/distances[6]+1/distances[5] + 1 / distances[4] + \
                1 / distances[3] + 1 / distances[2] + 1 / distances[0] + 1 / distances[1]:
            self.score = distances[4]  # διαλεγω καποιο κοστος,για τυχαιοτητα,απο τον πληθυσμο
            self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
            self.parents.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
    for _ in range(5): #για τον μερικο πληθυσμο
        self.score = distances[np.random.randint(0,10)] #τυχαια αυτη την φορα οχι ρουλετα γιατι δεν θα ειναι γονεις
        self.current_best = self.all_pop[distances.tolist().index(self.score)]  # και κραταω σε λιστα
        self.some_pop.append(self.current_best)  # συνενω τις λυσεις,τις θελω ολες,οχι μονο τις καλυτερες
    return distances


Population.choose_parents = choose_parents


def swap(chromosome):
    a, b = np.random.choice(len(chromosome), 2)  # διαλεγω απο τις 4ις ενδιαμεσες πολεις,τις δυο
    chromosome[a], chromosome[b] = (  # αλλαζω τις πολεις,ή το χρωμοσωμα
        chromosome[b],
        chromosome[a],
    )
    return chromosome  # επιστρεφω την συγκεκριμενη διαδρομη


def one_point_crossover(self):  # αλλος τροπος για την διαδικασια της αναπαραωγης
    children = []
    count, size = self.parents.shape  # size οσο οι πολεις
    for _ in range(len(self.parents)): # 5 θα γινουν γονεις
        parent1, parent2 = self.parents[  # διαλεγω 2(απο τα χρωμοσωματα των γονιων) με τυχαιο τροπο
                           np.random.randint(count, size=2), :  # απο τις 4ις πολεις
                           ]
        child = [None] * size  # αρχικοποιω το παιδι για να ειναι διαστασεων 4 με κενα,ωστε
        for i in range(1, 2, 1):  # εως το πρωτο σημειο γεμιζω με γονιδια του ενος γονεα,βγαινει στην μεση
            child[i] = parent1[i]  # να τα γεμισω με τις τιμες των γονιων
        pointer = 0  # κι μετα θελω εναν μετρητη
        for i in range(size):  # ωστε να μην εχω ιδια πολη στο χρωμοσωμα
            if child[i] is None:  # ελεγχω τις κενες θεσεις
                while parent2[pointer] in child:
                    pointer += 1  # π πριν την επαναληψη γεμιζω στο σημειο του Pointer
                child[i] = parent2[pointer]
        children.append(child)  # και το βαζω στα παιδια
    for _ in range(len(self.some_pop)): # και για τον αλλον μισο πληθυσμο που θα μεινει ιδιος
        some_pop = self.some_pop[np.random.randint(0,5)]
        child = [None] * size
        for i in range(0,4,1):
            child[i] = some_pop[i]
        children.append(child)
    return children


Population.one_point_crossover = one_point_crossover


def anaparagogi(self):  # επιλεγει ειτε mutation ειτε crossover ενος σημειου
    next_pop = []  # next gen population
    children = self.one_point_crossover()  # γινεται παντα
    for child in children:
        next_pop.append(child)
        if np.random.rand() < 0.01:  # για 1% πιθανοτητα καθε φορα που εκτελειται,
            # θα συμβαινει για καποιο ποσοστο στον πληθυσμο για καθε γενια
            next_pop.append(swap(child))  # βαζω τα νεα μεταλλαγμενα παιδια
            print("there has been a mutation!")
    return next_pop


Population.anaparagogi = anaparagogi


def genetic_algorithm(
        cities,
        routes,
        n=10,  # αρχικος πληθυσμος
        gen=10000,  # γενιες

):
    p = first_population(cities, routes, n)
    current_best = p.current_best
    score = float("inf")  # αρχικοποιω την καλυτερη λυση ως το απειρο
    current_route = []
    for i in range(gen):  # γενιες
        p.choose_parents()  # για 6 γονεις,ανανεωση 40%
        p.parents = np.asarray(p.parents)
        current_route.append(p.score)
        print(f"Generation {i}: {p.score}")
        if p.score < score:  # αν εχω νεο χαμηλοτερο σκορ
            current_best = p.current_best  # απο την λιστα των καλυτερων σκορ
            score = p.score
        children = p.anaparagogi()  # καλω την mutate και κανει ειτε crossover ειτε mutate στον ιδιο πληθυσμο
        if len(children) > 10:  # για σταθερο πληθυσμο 10,τα παλια παιδια διαγραφωνται,αφου καλω την συναρτηση για τα παιδια
            del (children[0:len(children) - 10])  # για την νεα γενια
        p = Population(children, p.routes)
        if score <= 16:  # μια αρκετα καλη λυση, 15 η βελτιστη
            break
    return current_best, current_route


current_best, current_route = genetic_algorithm(cities, routes)

plt.plot(range(len(current_route)), current_route, color="skyblue")
plt.show()
c1 = [0]
print(c1 + current_best + c1)  # 1 5 3 2 4 ,μπορει να εχει πολλαπλες
