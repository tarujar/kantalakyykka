/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Game } from '../models/Game';
import type { GameCreate } from '../models/GameCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class GamesService {
    /**
     * List Games
     * @returns Game Successful Response
     * @throws ApiError
     */
    public static listGamesApiV1GamesGet(): CancelablePromise<Array<Game>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/games/',
        });
    }
    /**
     * Create Game
     * @param requestBody
     * @returns Game Successful Response
     * @throws ApiError
     */
    public static createGameApiV1GamesPost(
        requestBody: GameCreate,
    ): CancelablePromise<Game> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/games/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Game
     * @param gameId
     * @returns Game Successful Response
     * @throws ApiError
     */
    public static getGameApiV1GamesGameIdGet(
        gameId: number,
    ): CancelablePromise<Game> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/games/{game_id}',
            path: {
                'game_id': gameId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
