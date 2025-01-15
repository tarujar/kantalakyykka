/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Player } from '../models/Player';
import type { PlayerCreate } from '../models/PlayerCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class PlayersService {
    /**
     * List Players
     * @returns Player Successful Response
     * @throws ApiError
     */
    public static listPlayersApiV1PlayersGet(): CancelablePromise<Array<Player>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/players/',
        });
    }
    /**
     * Create Player
     * @param requestBody
     * @returns Player Successful Response
     * @throws ApiError
     */
    public static createPlayerApiV1PlayersPost(
        requestBody: PlayerCreate,
    ): CancelablePromise<Player> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/players/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Player
     * @param playerId
     * @returns Player Successful Response
     * @throws ApiError
     */
    public static getPlayerApiV1PlayersPlayerIdGet(
        playerId: number,
    ): CancelablePromise<Player> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/players/{player_id}',
            path: {
                'player_id': playerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Player
     * @param playerId
     * @param requestBody
     * @returns Player Successful Response
     * @throws ApiError
     */
    public static updatePlayerApiV1PlayersPlayerIdPut(
        playerId: number,
        requestBody: PlayerCreate,
    ): CancelablePromise<Player> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/players/{player_id}',
            path: {
                'player_id': playerId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Player
     * @param playerId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deletePlayerApiV1PlayersPlayerIdDelete(
        playerId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/players/{player_id}',
            path: {
                'player_id': playerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
