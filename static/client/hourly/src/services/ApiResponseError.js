/**
 * An APIResponseError is an error that is caught when the API
 * responds with a code that is not a 'success' error code.
 */
class APIResponseError extends Error {

    /**
     * Constructs a new APIResponseError.
     * @param {number} status
     * @param {JSON} json represents the json data containing the response
     * @param {string} message 
     */
    constructor(status, json, message) {
        super(message);
        this.statusCode = status;
        this.json = json;
        this.message = message
    }

    /**
     * Represents the status code.
     * @returns {number} status the status
     */
    getStatus() {
        return this.statusCode
    }

    /**
     * Returns the JSON data of the response.
     * @returns {JSON}
     */
    getJSON() {
        return this.json
    }

    /**
     * Returns the message.
     * @returns {JSON}
     */
    getMessage() {
        return this.message
    }

}