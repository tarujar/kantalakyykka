/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { GameType } from '../models/GameType';
import type { GameTypeCreate } from '../models/GameTypeCreate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class GameTypesService {
    /**
     * List Game Types
     * @returns GameType Successful Response
     * @throws ApiError
     */
    public static listGameTypesApiV1GameTypesGet(): CancelablePromise<Array<GameType>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/game_types/',
        });
    }
    /**
     * Create Game Type
     * @param requestBody
     * @returns GameType Successful Response
     * @throws ApiError
     */
    public static createGameTypeApiV1GameTypesPost(
        requestBody: GameTypeCreate,
    ): CancelablePromise<GameType> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/game_types/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Game Type
     * @param gameTypeId
     * @returns GameType Successful Response
     * @throws ApiError
     */
    public static getGameTypeApiV1GameTypesGameTypeIdGet(
        gameTypeId: number,
    ): CancelablePromise<GameType> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/game_types/{game_type_id}',
            path: {
                'game_type_id': gameTypeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Game Type
     * @param gameTypeId
     * @param requestBody
     * @returns GameType Successful Response
     * @throws ApiError
     */
    public static updateGameTypeApiV1GameTypesGameTypeIdPut(
        gameTypeId: number,
        requestBody: GameTypeCreate,
    ): CancelablePromise<GameType> {
        return __request(OpenAPI, {
            method: 'PUT',
            url: '/api/v1/game_types/{game_type_id}',
            path: {
                'game_type_id': gameTypeId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Game Type
     * @param gameTypeId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static deleteGameTypeApiV1GameTypesGameTypeIdDelete(
        gameTypeId: number,
    ): CancelablePromise<Record<string, any>> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/game_types/{game_type_id}',
            path: {
                'game_type_id': gameTypeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
