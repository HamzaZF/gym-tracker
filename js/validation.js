// Récupération des éléments interactifs
const buttonsFinish = document.querySelectorAll('.btn-finish');
const buttonsNotFinish = document.querySelectorAll('.btn-not-finish');
const validateButton = document.getElementById('validate-button');
const resetButton = document.getElementById('reset-button');
let isLocked = false; // Verrouillage global après validation

// Fonction pour vérifier si tous les exercices ont été évalués
function allExercisesSelected() {
    const exercises = document.querySelectorAll('.card'); // Sélection de toutes les cartes
    for (let exercise of exercises) {
        const finishSelected = exercise.querySelector('.btn-finish.selected');
        const notFinishSelected = exercise.querySelector('.btn-not-finish.selected');
        // Si un exercice n'a pas de bouton sélectionné, retourner false
        if (!finishSelected && !notFinishSelected) {
            return false;
        }
    }
    return true; // Tous les exercices ont été évalués
}

// Gestion des boutons "Terminé" et "Non Terminé"
buttonsFinish.forEach(button => {
    button.addEventListener('click', () => {
        if (!isLocked) {
            button.classList.add('selected'); // Marquer ce bouton comme sélectionné
            button.nextElementSibling.classList.remove('selected'); // Désélectionner l'autre bouton
        }
    });
});

buttonsNotFinish.forEach(button => {
    button.addEventListener('click', () => {
        if (!isLocked) {
            button.classList.add('selected'); // Marquer ce bouton comme sélectionné
            button.previousElementSibling.classList.remove('selected'); // Désélectionner l'autre bouton
        }
    });
});

// Gestion du bouton "Valider"
validateButton.addEventListener('click', () => {
    if (!isLocked) {
        if (allExercisesSelected()) {
            isLocked = true; // Verrouiller les sélections après validation
            validateButton.classList.add('disabled'); // Désactiver le bouton "Valider"
            resetButton.classList.remove('disabled'); // Activer le bouton "Annuler"

            // Désactiver tous les boutons non sélectionnés
            buttonsFinish.forEach(button => {
                if (!button.classList.contains('selected')) {
                    button.classList.add('disabled');
                }
            });

            buttonsNotFinish.forEach(button => {
                if (!button.classList.contains('selected')) {
                    button.classList.add('disabled');
                }
            });

            alert("Exercices validés !");
        } else {
            alert("Veuillez sélectionner une option pour tous les exercices avant de valider !");
        }
    }
});

// Gestion du bouton "Annuler"
resetButton.addEventListener('click', () => {
    if (isLocked) {
        isLocked = false; // Déverrouiller les choix
        validateButton.classList.remove('disabled'); // Réactiver le bouton "Valider"
        resetButton.classList.add('disabled'); // Désactiver le bouton "Annuler"

        // Réinitialiser les sélections
        buttonsFinish.forEach(button => {
            button.classList.remove('selected', 'disabled');
        });

        buttonsNotFinish.forEach(button => {
            button.classList.remove('selected', 'disabled');
        });
    }
});
