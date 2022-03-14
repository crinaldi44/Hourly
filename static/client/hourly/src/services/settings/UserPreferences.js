/**
 * User preferences represent preferences of the active user that are persisted
 * locally via localStorage, indexedDB, or session storage. Generally, values
 * that are obtained via local storage will be managed here via helper classes
 * so as to maintain a consistent flow of control throughout the application.
 * @author chrisrinaldi
 * @since 13 March, 2022
 */
class UserPreferences {


    /**
     * Represents the default settings to persist
     * to the local storage.
     */
    defaults = {
        colorScheme: {
            type: 'string',
            value: '#2A3448'
        },
        appbarLight: {
            type: 'boolean',
            value: 'false'
        }
    }

    /**
     * Constructs a new UserPreferences object.
     */
    constructor() {

    }


    /**
     * Saves the user preference.
     * @param preference represents the preference to save
     */
    save(preference, value) {

        // Check that the preference specified is valid.
        if (!Object.keys(this.defaults).includes(preference)) {
            throw new Error(`Invalid preference specified! Syntax error on: ${preference}`);
        } else if (!(typeof value === typeof this.defaults[preference].type)) {
            // Type check.
            throw new Error(`Type mismatch: preference ${preference} expects type ${this.defaults[preference].type}`);
        } else {
            localStorage.setItem(preference, value);
        }
    }

    /**
     * Retrieves the specified preference from localStorage.
     * @param {string} preference represents the preference
     */
    get(preference) {
        if (!(typeof preference === 'string')) {
            throw new Error('Must specify a string to retrieve a user preference!');
        } else {
            if (localStorage.getItem(preference)) return localStorage.getItem(preference)
            else return null;
        }
    }

    /**
     * Represents whether the user has the specified preference set.
     * @param {string} preference 
     * @returns 
     */
    hasPreferenceSet(preference) {
        if (!(typeof preference === 'string')) {
            throw new Error('Must specify a string to retrieve a user preference!');
        } else {
            return localStorage.getItem(preference) !== null;
        }
    }

    /**
     * Resets all user-specified preferences. Note, this
     * method will clear all user preferences that are
     * specified in the defaults object.
     */
    reset() {
        for (const pref in Object.keys(this.defaults)) {
            localStorage.removeItem(pref);
        }
    }

    /**
     * Deletes the specified preference from localStorage.
     * @param {string} preference represents the preference
     * @returns {void}
     */
    delete(preference) {
        if (!localStorage.getItem(preference)) {
            return;
        } else {
            localStorage.removeItem(preference);
        }
    }

}

// Export an instance of the UserPreferences class.
export default new UserPreferences();