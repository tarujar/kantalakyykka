/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { Series } from '../models/Series';
import type { SeriesCreate } from '../models/SeriesCreate';
import type { TeamInSeries } from '../models/TeamInSeries';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class SeriesService {
    /**
     * List Series
     * @returns Series Successful Response
     * @throws ApiError
     */
    public static listSeriesApiV1SeriesGet(): CancelablePromise<Array<Series>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/series/',
        });
    }
    /**
     * Create Series
     * @param requestBody
     * @returns Series Successful Response
     * @throws ApiError
     */
    public static createSeriesApiV1SeriesPost(
        requestBody: SeriesCreate,
    ): CancelablePromise<Series> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/series/',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Series
     * @param seriesId
     * @returns Series Successful Response
     * @throws ApiError
     */
    public static getSeriesApiV1SeriesSeriesIdGet(
        seriesId: number,
    ): CancelablePromise<Series> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/series/{series_id}',
            path: {
                'series_id': seriesId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Team To Series
     * @param seriesId
     * @param requestBody
     * @returns TeamInSeries Successful Response
     * @throws ApiError
     */
    public static addTeamToSeriesApiV1SeriesSeriesIdTeamsPost(
        seriesId: number,
        requestBody: TeamInSeries,
    ): CancelablePromise<TeamInSeries> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/series/{series_id}/teams',
            path: {
                'series_id': seriesId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Add Player To Team
     * @param seriesId
     * @param teamId
     * @param playerId
     * @returns any Successful Response
     * @throws ApiError
     */
    public static addPlayerToTeamApiV1SeriesSeriesIdTeamsTeamIdPlayersPost(
        seriesId: number,
        teamId: number,
        playerId: number,
    ): CancelablePromise<any> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/series/{series_id}/teams/{team_id}/players',
            path: {
                'series_id': seriesId,
                'team_id': teamId,
            },
            query: {
                'player_id': playerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
