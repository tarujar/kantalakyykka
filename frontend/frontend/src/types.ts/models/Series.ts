/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type Series = {
    id: number;
    name: string;
    season_type: Series.season_type;
    year: number;
    status: ('upcoming' | 'ongoing' | 'completed' | null);
    registration_open: (boolean | null);
    game_type_id: number;
    created_at: (string | null);
};
export namespace Series {
    export enum season_type {
        SUMMER = 'summer',
        WINTER = 'winter',
    }
}

