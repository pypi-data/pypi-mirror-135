# Utilitaire de contrôle de Kubernetes

> ** What is this ??? **
> Every time we use a word in English our manager tells us to use the French translation of it. So, here is a version of kubectl ... in French !

### Parce que quelques exemples valent mieux que mille mots 

kubectl get pods : 
```shell
$ kubectlfr récupérer gousses
NAME                                                              READY    STATUS          RESTARTS      AGE
ceci-est-une-gousse                                                1/1     Running            0          1h
...
ceci-est-une-autre-gousse                                          1/1     Running            0           9d

```

kubectl create namespace test : 
```shell
$ kubectlfr créer espace-de-nom test
namespace/test created
```

### Informations générales

Le fonctionnement est très simple : `kubectlfr` traduit les mots qu'il a dans son dictionnaire puis les passe à `kubectl`. Vous pouvez donc utiliser `kubectlfr` exactement vous utilisez `kubectl` tout en vous gardant la possibilité de défendre le beau pays du vin et du fromage.

Vous pourrez retrouver tous les mots traduits [ici](https://github.com/theophanevie/kubectlfr/blob/main/kubectlfr/translation.py).

N'hésitez pas à en ajouter, Molière sera fier de vous ! Attention aux accents et au pluriel !
