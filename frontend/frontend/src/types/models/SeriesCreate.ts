/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type SeriesCreate = {
    name: string;
    season_type: SeriesCreate.season_type;
    year: number;
    status?: ('upcoming' | 'ongoing' | 'completed' | null);
    registration_open?: (boolean | null);
    game_type_id: number;
};
export namespace SeriesCreate {
    export enum season_type {
        SUMMER = 'summer',
        WINTER = 'winter',
    }
}

